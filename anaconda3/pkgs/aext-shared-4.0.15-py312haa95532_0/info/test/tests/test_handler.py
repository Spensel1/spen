import json
from http.cookies import SimpleCookie
from typing import Dict, Optional, Type
from unittest.mock import patch

import jwt
import respx
import tornado.web
from anaconda_cloud_auth.exceptions import TokenNotFoundError
from anaconda_cloud_auth.token import TokenInfo
from httpx import Request, Response
from jupyter_server.auth.identity import IdentityProvider
from tornado.httpclient import HTTPResponse
from tornado.testing import AsyncHTTPTestCase

import aext_shared.handler
from aext_shared.handler import BackendError, BackendHandler, create_rules


class GoodHandler(BackendHandler):
    @tornado.web.authenticated
    async def get(self):
        self.finish({"hello": "world"})


class AnacondaCloudHandler(BackendHandler):
    @tornado.web.authenticated
    async def get(self):
        response = await self.anaconda_cloud_proxy("account", method="GET", headers={"cloud_header": "cloud_value"})
        self.finish(response)


class AnacondaPublicHandler(BackendHandler):
    @tornado.web.authenticated
    async def get(self):
        response = await self.anaconda_cloud_proxy("public_data", method="GET", auth_optional=True)
        self.finish(response)


class RaisesHttpErrorHandler(BackendHandler):
    @tornado.web.authenticated
    async def get(self):
        status_code = int(self.request.headers.get("Response-Code", "500"))
        raise tornado.web.HTTPError(status_code=status_code, log_message="uh oh")


class RaisesBackendErrorHandler(BackendHandler):
    @tornado.web.authenticated
    async def get(self):
        status_code = int(self.request.headers.get("Response-Code", "500"))
        data = json.loads(self.request.headers.get("Response-Payload", "{}"))
        log_message = self.request.headers.get("Log-Message", None)
        raise BackendError(status_code, data, log_message)


class TestBackendHandler(AsyncHTTPTestCase):
    def setUp(self):
        # Mocked anaconda.cloud API httpx responses
        aext_shared.handler.extra_anaconda_headers = {
            "testbackendhandler": "extra_header",
            "testbackendhandler2": "extra_header2",
        }
        self.account_response = Response(
            status_code=200,
            json={
                "profile": {"is_confirmed": True, "is_disabled": False},
                "subscriptions": [
                    {"id": "sub_1"},
                    {"id": "sub_2"},
                ],
                "user": {"id": "user_1", "email": "snek@anaconda.com"},
            },
        )
        self.token_response = Response(
            status_code=200,
            json={
                "access_token": "deadbeef",
                "expires_in": 2000,
            },
        )
        self.mocked_api = respx.mock(base_url="https://anaconda.cloud/api/", assert_all_called=False)
        self.mocked_api.get("account").mock(side_effect=self.account_side_effect)
        self.mocked_api.post("iam/token").mock(side_effect=self.token_side_effect)
        self.mocked_api.get("public_data").mock(return_value=self.account_response)
        self.mocked_api.start()
        super().setUp()

    def tearDown(self) -> None:
        aext_shared.handler.extra_anaconda_headers = {}
        self.mocked_api.stop()
        return super().tearDown()

    def account_side_effect(self, request: Request) -> Response:
        if request.headers.get("Authorization") == "Bearer deadbeef":
            return self.account_response
        return Response(status_code=401)

    def token_side_effect(self, request: Request) -> Response:
        payload = json.loads(request.content)
        if payload.get("refresh_token") == "xyz":
            return self.token_response
        return Response(status_code=400, json="oh no")

    def get_app(self):
        handlers: Dict[str, Type[BackendHandler]] = {
            "good": GoodHandler,
            "anaconda": AnacondaCloudHandler,
            "anaconda_public": AnacondaPublicHandler,
            "raise_http_error": RaisesHttpErrorHandler,
            "raise_backend_error": RaisesBackendErrorHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    def test_good_handler(self):
        headers = {"Authorization": "token abc"}
        response = self.fetch("/good", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {"hello": "world"}

    def test_anaconda_handler_missing_refresh_token(self):
        headers = {"Authorization": "token abc"}

        @classmethod
        def mock_load(cls, domain):
            raise TokenNotFoundError

        with patch.object(TokenInfo, "load", mock_load):
            response = self.fetch("/anaconda", headers=headers)
        assert response.code == 403
        assert json.loads(response.body) == {"reason": "missing refresh_token"}

    def test_anaconda_handler_valid_access_token(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(access_token="deadbeef", refresh_token="xyz"),
        }
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "remote_data": self.account_response.json(),
            "remote_status_code": 200,
        }

    def test_anaconda_handler_valid_access_token_bad_refresh_token(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(access_token="deadbeef", refresh_token="bad_refresh_token"),
        }
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "remote_data": self.account_response.json(),
            "remote_status_code": 200,
        }

    def test_anaconda_handler_valid_refresh_token_only(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(refresh_token="xyz"),
        }
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert get_access_cookie_from_response(response) == "deadbeef"
        assert json.loads(response.body) == {
            "remote_data": self.account_response.json(),
            "remote_status_code": 200,
        }
        for call in self.mocked_api.calls:
            assert call.request.headers.get("testbackendhandler") == "extra_header"
            assert call.request.headers.get("testbackendhandler2") == "extra_header2"

    def test_anaconda_handler_invalid_refresh_token_only(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(refresh_token="invalid"),
        }
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 403
        assert json.loads(response.body) == {
            "remote_status_code": 400,
            "reason": "proxy_bad_response",
            "remote_data": "oh no",
        }

    def test_anaconda_handler_expired_access_token(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(access_token="expired", refresh_token="xyz"),
        }
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "remote_data": self.account_response.json(),
            "remote_status_code": 200,
        }
        assert get_access_cookie_from_response(response) == "deadbeef"
        assert self.mocked_api.calls.last.request.headers.get("cloud_header") == "cloud_value"

    def test_anaconda_handler_api_key(self):
        """We can also use an API key for authentication."""
        headers = {
            "Authorization": "token abc",  # Doesn't matter what it is
        }

        @classmethod
        def mock_load(cls, domain):
            return TokenInfo(api_key="deadbeef", domain=domain)

        with patch.object(TokenInfo, "load", mock_load):
            response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "remote_data": self.account_response.json(),
            "remote_status_code": 200,
        }

    def test_anaconda_handler_expired_access_token_and_bad_refresh_token(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(access_token="expired", refresh_token="bad_refresh_token"),
        }
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 403
        assert json.loads(response.body) == {
            "remote_status_code": 400,
            "reason": "proxy_bad_response",
            "remote_data": "oh no",
        }
        assert get_access_cookie_from_response(response) is None

    def test_anaconda_handler_return_400(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(access_token="deadbeef", refresh_token="xyz"),
        }
        self.account_response = Response(
            status_code=400,
            json={"message": "some downstream error"},
        )
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "reason": "proxy_bad_response",
            "remote_status_code": 400,
            "remote_data": self.account_response.json(),
        }
        assert self.mocked_api.calls.last.request.headers.get("cloud_header") == "cloud_value"

    def test_anaconda_handler_expired_access_token_return_400(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(access_token="expired", refresh_token="xyz"),
        }
        self.account_response = Response(
            status_code=400,
            json={"message": "some downstream error"},
        )
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "reason": "proxy_bad_response",
            "remote_status_code": 400,
            "remote_data": self.account_response.json(),
        }

    def test_anaconda_handler_only_refresh_token_downstream_returns_403(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(refresh_token="xyz"),
        }
        self.account_response = Response(
            status_code=403,
            json={"message": "downstream says unauthorized"},
        )
        response = self.fetch("/anaconda", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "reason": "proxy_bad_response",
            "remote_status_code": 403,
            "remote_data": self.account_response.json(),
        }
        assert get_access_cookie_from_response(response) == "deadbeef"

    def test_raise_http_400(self):
        headers = {"Authorization": "token abc", "Response-Code": "400"}
        response = self.fetch("/raise_http_error", headers=headers)
        assert response.code == 400
        assert json.loads(response.body) == {"reason": "unknown"}

    def test_raise_http_502(self):
        headers = {"Authorization": "token abc", "Response-Code": "502"}
        response = self.fetch("/raise_http_error", headers=headers)
        assert response.code == 502
        assert json.loads(response.body) == {"reason": "unknown"}

    def test_raise_unknown_backend_400(self):
        headers = {
            "Authorization": "token abc",
            "Response-Code": "400",
            "Response-Payload": json.dumps({"other": "data"}),
        }
        response = self.fetch("/raise_backend_error", headers=headers)
        assert response.code == 400
        assert json.loads(response.body) == {"reason": "unknown", "other": "data"}

    def test_raise_backend_500_with_reason(self):
        headers = {
            "Authorization": "token abc",
            "Response-Code": "500",
            "Response-Payload": json.dumps({"reason": "nope", "other": "data"}),
        }
        response = self.fetch("/raise_backend_error", headers=headers)
        assert response.code == 500
        assert json.loads(response.body) == {"reason": "nope", "other": "data"}

    def test_auth_optional_200_without_auth(self):
        headers = {
            "Authorization": "token abc",
        }
        response = self.fetch("/anaconda_public", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "remote_data": self.account_response.json(),
            "remote_status_code": 200,
        }

    def test_auth_optional_200_with_only_refresh_token(self):
        headers = {
            "Authorization": "token abc",
            "Cookie": _to_cookie(refresh_token="xyz"),
        }
        response = self.fetch("/anaconda_public", headers=headers)
        assert response.code == 200
        assert json.loads(response.body) == {
            "remote_data": self.account_response.json(),
            "remote_status_code": 200,
        }
        assert get_access_cookie_from_response(response) == "deadbeef"


def test_backend_error_unknown_reason():
    err = BackendError(status_code=400, data={})
    assert str(err) == "BackendError 400: unknown"


def test_backend_error_with_reason():
    err = BackendError(status_code=400, data={"reason": "nope"})
    assert str(err) == "BackendError 400: nope"


def test_backend_error_custom_message():
    err = BackendError(status_code=400, data={"reason": "nope"}, log_message="custom message")
    assert str(err) == "custom message"


def test_is_token_expired():
    assert (
        BackendHandler._is_token_expired(
            "eyJhbGciOiJSUzI1NiIsImtpZCI6ImRlZmF1bHQiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3MDcyOTg3NTYsInN1YiI6ImU3NjFkYTU4LTczMmUtNDk0My1hZjQwLTVkNGNhYmE0MWJmZSJ9.etZ_HMmCBbcTlUT4CEGmd1H0ov4L0To2-ldNltG1whM2KwG9U9wXgTi61kkd4Lv9eTChzELCTDuAVSFEA0eCwrC4txCO_Y4yUU6CuAmbR7s0tbtB599s7u44m_sj8IxrzF_IoyTgfU-WAgNhEXnDNWo33X8ZR174EteN1Ol_FvFQo-mhKDLRyIJkewFFpxepsfCLz3wYnpBAq8XBIzmtYBSnkByKH8sPE-FAGM2Z8HLXY7j8vGY1cORm5dM-Anlis_ffy-3jnoaaFzOXeCqlaR1xp_2ShDgx01E76h9wDIhHhCbyhaRtmnn7wS3mkKuqMNLN0GO3QgtmtbH4BH67aw"
        )
        is True
    )


def get_access_cookie_from_response(response: HTTPResponse) -> Optional[str]:
    headers = response.headers.get_list("Set-Cookie")
    access_token = None
    for header in headers:
        cookie = SimpleCookie()
        cookie.load(header)
        # Make sure we don't try to set the access_token twice
        assert (access_token is None) or (cookie.get("access_token") is None)
        val = cookie.get("access_token")
        if val is not None:
            access_token = val.value
    return access_token


def _to_cookie(access_token: Optional[str] = None, refresh_token: Optional[str] = None):
    vals = {"access_token": access_token, "refresh_token": refresh_token}
    return "; ".join([f"{key}={value}" for key, value in vals.items() if value is not None])
