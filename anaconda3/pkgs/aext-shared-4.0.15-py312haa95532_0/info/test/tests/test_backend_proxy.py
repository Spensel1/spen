import json

import httpx
import pytest
from respx import MockRouter
from tornado.httpclient import HTTPRequest
from tornado.httputil import HTTPHeaders

from aext_shared.backend_proxy import ProxyResponse, backend_proxy
from aext_shared.errors import BackendError, BadRequest, UnknownError


@pytest.fixture()
def incoming():
    return HTTPRequest(
        "https://example.com",
        headers={"User-Agent": "firefox", "Api-Version": "2023-02-25"},
    )


async def test_allows_user_agent_override(respx_mock: MockRouter, incoming):
    respx_mock.get()
    headers = {"User-Agent": "abc"}
    assert await backend_proxy(incoming, "https://anaconda.cloud/api", headers=headers) == ProxyResponse(
        remote_status_code=200, remote_data=None
    )
    # Ensure the original request headers weren't modified
    assert headers["User-Agent"] == "abc"
    proxy_request = respx_mock.calls.last.request
    assert proxy_request.headers["User-Agent"] == "abc"


async def test_allows_api_version_override_with_http_headers(respx_mock: MockRouter, incoming):
    respx_mock.get()
    headers = HTTPHeaders({"Api-Version": "abc"})
    assert await backend_proxy(incoming, "https://anaconda.cloud/api", headers=headers) == ProxyResponse(
        remote_status_code=200, remote_data=None
    )
    proxy_request = respx_mock.calls.last.request
    assert proxy_request.headers["Api-Version"] == "abc"


async def test_connection_error(respx_mock: MockRouter, incoming):
    respx_mock.get().mock(side_effect=httpx.ReadTimeout("Unable to read within timeout"))
    with pytest.raises(UnknownError, match="proxy_connection_error"):
        await backend_proxy(incoming, "https://anaconda.cloud/api")


async def test_valid_no_content(respx_mock: MockRouter, incoming):
    respx_mock.get().respond(200)
    headers = {}
    assert await backend_proxy(incoming, "https://anaconda.cloud/api", headers=headers) == ProxyResponse(
        remote_status_code=200, remote_data=None
    )

    # Ensure the original request headers weren't modified
    assert headers == {}
    # But make sure the user agent was passed through
    proxy_request = respx_mock.calls.last.request
    assert proxy_request.headers["User-Agent"] == "firefox"


async def test_400_no_content(respx_mock: MockRouter, incoming):
    respx_mock.get().respond(status_code=400)
    with pytest.raises(BackendError) as exc_info:
        await backend_proxy(incoming, "https://anaconda.cloud/api")
    assert isinstance(exc_info.value, BackendError)
    assert exc_info.value.status_code == 200
    assert exc_info.value.data == {
        "remote_status_code": 400,
        "remote_data": None,
        "reason": "proxy_bad_response",
    }


async def test_valid_with_json(respx_mock: MockRouter, incoming):
    respx_mock.get().respond(json={"hello": "world"})
    assert await backend_proxy(incoming, "https://anaconda.cloud/api") == ProxyResponse(
        remote_status_code=200, remote_data={"hello": "world"}
    )


async def test_send_json_to_proxy(respx_mock: MockRouter, incoming):
    respx_mock.post().respond(json={"command": "pong"})
    assert await backend_proxy(
        incoming, "https://anaconda.cloud/api", json={"command": "ping"}, method="POST"
    ) == ProxyResponse(remote_status_code=200, remote_data={"command": "pong"})
    proxy_request = respx_mock.calls.last.request
    assert proxy_request.headers["Content-Type"] == "application/json"
    assert proxy_request.content == json.dumps({"command": "ping"}).encode("utf-8")


async def test_500_with_json(respx_mock: MockRouter, incoming):
    respx_mock.get().respond(
        status_code=500,
        json={"reason": "nope"},
    )
    with pytest.raises(BackendError) as exc_info:
        await backend_proxy(incoming, "https://anaconda.cloud/api")
    assert isinstance(exc_info.value, BackendError)
    assert exc_info.value.status_code == 200
    assert exc_info.value.data == {
        "remote_status_code": 500,
        "remote_data": {"reason": "nope"},
        "reason": "proxy_bad_response",
    }


async def test_valid_with_bad_json_response(respx_mock: MockRouter, incoming):
    respx_mock.get().respond(text="[not_json}")
    with pytest.raises(BadRequest, match="proxy_response_not_json"):
        await backend_proxy(incoming, "https://anaconda.cloud/api")


async def test_502_with_bad_json_response(respx_mock: MockRouter, incoming):
    respx_mock.get().respond(
        status_code=502,
        text="[not_json}",
    )
    with pytest.raises(BadRequest, match="proxy_response_not_json"):
        await backend_proxy(incoming, "https://anaconda.cloud/api")
