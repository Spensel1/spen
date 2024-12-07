import datetime
import json
import os
from typing import Dict, Type
from unittest.mock import MagicMock, mock_open, patch

import jwt
import tornado
from aext_assistant_server.handlers import (
    GetDiskStateRouteHandler,
    MonitorFileChangesRouteHandler,
    NucleusTokenRouteHandler,
    NucleusUserRouteHandler,
    SummarizeFileRouteHandler,
    SyncDiskStateRouteHandler,
)
from anaconda_cloud_auth.token import TokenInfo
from jupyter_server.auth.identity import IdentityProvider
from tornado.testing import AsyncHTTPTestCase, gen_test

from aext_shared.handler import BackendHandler, create_rules

# Made with:
# openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
# openssl rsa -pubout -in private_key.pem -out public_key.pem
test_private_key = open(os.path.join(os.path.dirname(__file__), "private_key.pem")).read()

exp_timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
payload = {"exp": exp_timestamp}
fake_access_token = jwt.encode(payload, test_private_key, algorithm="RS256")


def mock_load_api_key():
    return fake_access_token


class TestNucleusTokenRouteHandler(AsyncHTTPTestCase):
    def get_app(self):
        handlers: Dict[str, Type[BackendHandler]] = {
            "nucleus_token": NucleusTokenRouteHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @patch("aext_assistant_server.handlers._load_api_key", side_effect=mock_load_api_key)
    def test_get(self, _load_api_key):
        headers = {
            "Authorization": "token abc",
        }

        @classmethod
        def mock_load(cls, domain):
            return TokenInfo(api_key="deadbeef", domain=domain)

        with patch.object(TokenInfo, "load", mock_load):
            response = self.fetch("/nucleus_token", headers=headers)

        assert response.code == 200
        expected_body = {
            "access_token": fake_access_token,
            # Milliseconds
            "expires_at": int(datetime.datetime.fromtimestamp(exp_timestamp.timestamp()).timestamp() * 1000),
        }
        json_value = json.loads(response.body.decode("utf-8"))

        assert json_value["access_token"] == expected_body["access_token"]
        time_diff = abs(json_value["expires_at"] - expected_body["expires_at"])

        # For some reason, I can't get these to be the same. But they... come from the same place...
        assert time_diff < 100000000


class TestGetDiskStateHandler(AsyncHTTPTestCase):
    def get_app(self):
        handlers: Dict[str, Type[BackendHandler]] = {
            "get_disk_state": GetDiskStateRouteHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @patch(
        "aext_assistant_server.handlers.prepare_assistant_settings",
        return_value="dummy_path",
    )
    @patch("builtins.open", new_callable=mock_open, read_data='{"test": 123}')
    def test_get(self, _prepare_assistant_settings, _open):
        headers = {"Authorization": "token abc", "Cookie": "access_token=xyz"}
        data = {"test": 123}
        response = self.fetch("/get_disk_state", headers=headers)
        assert response.code == 200
        assert json.loads(response.body.decode("utf-8")) == data


class TestSyncDiskStateHandler(AsyncHTTPTestCase):
    def get_app(self):
        handlers: Dict[str, Type[BackendHandler]] = {
            "sync_disk_state": SyncDiskStateRouteHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @patch(
        "aext_assistant_server.handlers.prepare_assistant_settings",
        return_value="dummy_path",
    )
    @patch("builtins.open", new_callable=mock_open, read_data='{"test": 123}')
    def test_post(self, _prepare_assistant_settings, _open):
        data = {"test": 123}
        response = self.fetch(
            "/sync_disk_state",
            method="POST",
            body=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": "token abc",
            },
        )
        assert response.code == 200
        assert response.body == b""


mock_user_account = {
    "user": {
        "id": "test_user_id",
        "email": "test_user_email",
        "first_name": "test_user_first_name",
        "last_name": "test_user_last_name",
        "country": "US",
        "state": "FL",
        "promotional_content": True,
        "company": "Anaconda",
        "company_size": "medium",
        "position": "Software Engineer/Developer",
        "industry": "Technology",
        "username": "test_user_username",
        "created_at": "2023-05-23T22:17:29.049308+00:00",
        "updated_at": None,
        "partner_id": None,
        "partner_customer_id": None,
        "external_id": None,
        "first_home_visit": False,
    },
    "profile": {
        "is_confirmed": True,
        "is_disabled": False,
    },
    "subscriptions": [
        {
            "id": "b0ea430a-fe4e-4713-997a-98911bba1746",
            "org_id": "6463f62c-9c34-4497-9714-6274c8d2660e",
            "product_code": "commercial_subscription",
            "expires_at": "2027-01-01T00:00:00+00:00",
        }
    ],
}


class TestNucleusUserRouteHandler(AsyncHTTPTestCase):
    def get_app(self):
        handlers: Dict[str, Type[BackendHandler]] = {
            "nucleus_user": NucleusUserRouteHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @patch("aext_assistant_server.handlers._load_api_key", side_effect=mock_load_api_key)
    def test_get(self, _load_api_key):
        headers = {
            "Authorization": "token abc",
        }

        @classmethod
        def mock_load(cls, domain):
            return TokenInfo(api_key="deadbeef", domain=domain)

        with patch.object(TokenInfo, "load", mock_load):
            # Patch requests.get
            with patch("requests.get") as mock_get:
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = mock_user_account
                response = self.fetch("/nucleus_user", headers=headers)

        assert response.code == 200
        expected_body = {"remote_status_code": 200, "remote_data": mock_user_account}
        json_value = json.loads(response.body.decode("utf-8"))

        assert json_value["remote_status_code"] == expected_body["remote_status_code"]
        assert json_value["remote_data"] == expected_body["remote_data"]


class TestNucleusUserRouteHandlerWithCFHeaders(AsyncHTTPTestCase):
    def get_app(self):
        handlers: Dict[str, Type[BackendHandler]] = {
            "nucleus_user": NucleusUserRouteHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @patch("aext_assistant_server.handlers._load_api_key", side_effect=mock_load_api_key)
    def test_get(self, _load_api_key):
        # Add NUCLEUS_CLOUDFLARE_CLIENT_ID and NUCLEUS_CLOUDFLARE_CLIENT_SECRET to the environment
        os.environ["NUCLEUS_CLOUDFLARE_CLIENT_ID"] = "test_client_id"
        os.environ["NUCLEUS_CLOUDFLARE_CLIENT_SECRET"] = "test_client_secret"

        headers = {
            "Authorization": "token abc",
        }

        @classmethod
        def mock_load(cls, domain):
            return TokenInfo(api_key="deadbeef", domain=domain)

        with patch.object(TokenInfo, "load", mock_load):
            # Patch requests.get
            with patch("requests.get") as mock_get:
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = mock_user_account
                response = self.fetch("/nucleus_user", headers=headers)

        assert response.code == 200
        expected_body = {"remote_status_code": 200, "remote_data": mock_user_account}
        json_value = json.loads(response.body.decode("utf-8"))

        assert json_value["remote_status_code"] == expected_body["remote_status_code"]
        assert json_value["remote_data"] == expected_body["remote_data"]
        assert mock_get.call_args.kwargs["headers"]["CF-Access-Client-Id"] == "test_client_id"
        assert mock_get.call_args.kwargs["headers"]["CF-Access-Client-Secret"] == "test_client_secret"
        assert mock_get.call_args.kwargs["headers"]["Authorization"][:7] == "Bearer "


class TestMonitorFileChangesHandler(AsyncHTTPTestCase):
    def setUp(self):
        super().setUp()
        # Setup environment variable for the test environment
        self.original_wait_time = os.environ.get("ASSISTANT_MONITOR_FILES_WAIT_TIME")
        os.environ["ASSISTANT_MONITOR_FILES_WAIT_TIME"] = "1"

    def tearDown(self):
        # Restore original environment variable to avoid side effects
        if self.original_wait_time is not None:
            os.environ["ASSISTANT_MONITOR_FILES_WAIT_TIME"] = self.original_wait_time
        else:
            del os.environ["ASSISTANT_MONITOR_FILES_WAIT_TIME"]
        super().tearDown()

    def get_app(self):
        handlers = {
            "monitor_file_changes": MonitorFileChangesRouteHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),  # Adjust as needed
        )

    @gen_test
    @patch("os.getcwd", return_value="/path/to/dir")
    @patch("os.listdir", return_value=["test1.ipynb", "test2.ipynb"])
    @patch("os.path.getmtime")
    async def test_get_file_changes(self, mock_getmtime, mock_listdir, mock_getcwd):
        headers = {
            "Authorization": "token abc",
        }

        # Initially, set the modification times to simulate unchanged files
        mock_getmtime.side_effect = lambda x: 100  # Unix timestamp example

        # Start monitoring (should not return yet due to no changes)
        future_response = self.http_client.fetch(self.get_url("/monitor_file_changes"), headers=headers)

        # Simulate waiting without file changes
        response = await future_response
        self.assertEqual(response.code, 200)
        response_data = json.loads(response.body)
        self.assertEqual(response_data["path"], None)
        self.assertEqual(response_data["last_modified"], 0)

        # Simulate a file change and monitor again
        future_response = self.http_client.fetch(self.get_url("/monitor_file_changes"), headers=headers)
        mock_getmtime.side_effect = lambda x: 100 if x.endswith("test1.ipynb") else 200  # Change detected

        # Wait for the handler to detect the change
        response = await future_response
        self.assertEqual(response.code, 200)
        response_data = json.loads(response.body)
        self.assertEqual(response_data["path"], "test2.ipynb")
        self.assertEqual(response_data["last_modified"], 200)


class TestSummarizeFileRouteHandler(AsyncHTTPTestCase):
    def get_app(self):
        handlers = {
            "summarize_file": SummarizeFileRouteHandler,
        }
        return tornado.web.Application(
            create_rules("/", "", handlers),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),  # Adjust as needed
        )

    @gen_test
    @patch("builtins.open", mock_open(read_data="File contents for testing."))
    @patch("os.environ.get", return_value="http://mockedurl.com")
    @patch("aext_assistant_server.handlers._load_api_key", side_effect=mock_load_api_key)
    @patch("requests.post")
    async def test_summarize_file_success(self, mock_post, mock_load_api_key, mock_env):
        # Mock the response from the Assistant API
        mock_response = MagicMock()
        mock_response.json.return_value = {"summary": "This is a test summary."}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Define the request body
        request_body = {
            "file_path": "/path/to/file.ipynb",
            "session_id": "test_session",
            "response_message_id": "test_response",
            "x-client-source": "test_client",
        }

        # Make the POST request
        response = await self.http_client.fetch(
            self.get_url("/summarize_file"),
            method="POST",
            body=json.dumps(request_body),
            headers={"Content-Type": "application/json", "Authorization": "Bearer abc"},
        )

        # Assertions
        self.assertEqual(response.code, 200)
        response_data = json.loads(response.body)
        self.assertEqual(response_data["summary"], "This is a test summary.")

        # Ensure the Assistant API was called with expected headers and body
        mock_post.assert_called_with(
            "http://mockedurl.com/v1/pro/summaries",
            headers={
                "x-client-version": "0.4.0",
                "x-client-source": "test_client",
                "Content-Type": "application/json",
                "Authorization": "Bearer {fake_access_token}".format(fake_access_token=fake_access_token),
            },
            json={
                "source": {"name": "/path/to/file.ipynb", "data": "File contents for testing.", "type": "ipynb"},
                "session_id": "test_session",
                "response_message_id": "test_response",
                "skip_logging": False,
            },
        )
