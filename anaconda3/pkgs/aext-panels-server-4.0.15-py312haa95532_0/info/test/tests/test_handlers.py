import json
import urllib
from dataclasses import asdict
from unittest import mock

import aext_panels_server as panel
import respx
import tornado.web
from aext_panels_server.api import HeadersAndCookies
from aext_panels_server.schemas import (
    FileInfo,
    MetaResponse,
    RequestError,
    ServiceResponse,
)
from jupyter_server.auth.identity import IdentityProvider
from tornado.testing import AsyncHTTPTestCase


class TestHealthzHandler(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application(
            panel.get_routes("/"),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    def test_healthz_handler(self):
        headers = {"Authorization": "token abc"}
        response = self.fetch("/aext_panels_server/healthz", headers=headers)
        assert response.code == 200
        expected = {"live": True}
        assert json.loads(response.body) == expected


class TestProjectDownloadHandler(AsyncHTTPTestCase):
    success = {"archive": "zipfiles"}
    error = "error"

    def get_app(self):
        return tornado.web.Application(
            panel.get_routes("/"),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @respx.mock
    def test_download_project_files_v2_success(self):
        respx.get().respond(status_code=200, json=self.success)
        headers = {"Authorization": "token abc", "Cookie": "access_token=xyz", "X-MS-API-Version": "v2"}

        with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI._get_headers_and_cookies") as m:
            m.return_value = HeadersAndCookies(headers=headers, cookies={})

            response = self.fetch(
                "/aext_panels_server/projects/download?project_id=test-project&project_version=test-version",
                headers=headers,
            )
            assert response.code == 200
            assert json.loads(response.body) == asdict(
                ServiceResponse(meta=MetaResponse(RequestError(False)), content=self.success)
            )


class TestProjectActionHandler(AsyncHTTPTestCase):
    success = "success"
    error = "error"

    def get_app(self):
        return tornado.web.Application(
            panel.get_routes("/"),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @respx.mock
    def test_delete_project_v2_success(self):
        respx.delete().respond(status_code=204, json=self.success)
        headers = {"Authorization": "token abc", "Cookie": "access_token=xyz", "X-MS-API-Version": "v2"}

        with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI._get_headers_and_cookies") as m:
            m.return_value = HeadersAndCookies(headers=headers, cookies={})

            response = self.fetch(
                "/aext_panels_server/projects/test-project/delete/", method="POST", headers=headers, body=""
            )
            assert response.code == 200
            assert json.loads(response.body) == asdict(
                ServiceResponse(meta=MetaResponse(RequestError(False)), content={})
            )


class TestProjectVersionHandler(AsyncHTTPTestCase):
    success = "success"
    error = "error"

    def get_app(self):
        return tornado.web.Application(
            panel.get_routes("/"),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @respx.mock
    def test_get_project_notebook_v2_success(self):
        respx.get().respond(status_code=200, json=self.success)
        headers = {"Authorization": "token abc", "Cookie": "access_token=xyz", "X-MS-API-Version": "v2"}

        with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI._get_headers_and_cookies") as m:
            m.return_value = HeadersAndCookies(headers=headers, cookies={})

            response = self.fetch("/aext_panels_server/projects/test-project/version/test-version/", headers=headers)
            assert response.code == 200
            assert json.loads(response.body) == asdict(
                ServiceResponse(meta=MetaResponse(RequestError(False)), content=self.success)
            )

    @respx.mock
    def test_delete_project_notebook_v2_success(self):
        respx.delete().respond(status_code=204, json=self.success)
        headers = {"Authorization": "token abc", "Cookie": "access_token=xyz", "X-MS-API-Version": "v2"}

        with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI._get_headers_and_cookies") as m:
            m.return_value = HeadersAndCookies(headers=headers, cookies={})

            response = self.fetch(
                "/aext_panels_server/projects/test-project/version/test-version/", method="DELETE", headers=headers
            )
            assert response.code == 200
            assert json.loads(response.body) == asdict(
                ServiceResponse(meta=MetaResponse(RequestError(False)), content=self.success)
            )


class TestProjectHandler(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application(
            panel.get_routes("/"),
            cookie_secret="abc",
            identity_provider=IdentityProvider(token="abc"),
        )

    @respx.mock
    def test_create_project_should_call_log_notebook_data(self):
        respx.get().respond(status_code=200, json={})
        headers = {
            "Authorization": "token abc",
            "Cookie": "access_token=xyz; refresh_token=zyx",
            "X-MS-API-Version": "v1",
        }
        form_data = {
            "path": "backend_lib/panel/tests/assets/test-notebook.ipynb",
            "title": "nb",
            "version": "2024.03.1",
            "description": "",
            "environment": "anaconda-panel-2023.05-py310",
        }
        with mock.patch("aext_panels_server.base_handlers.PABaseHandler._evaluate_feature_flag") as meff:
            meff.return_value = True
            with mock.patch("aext_panels_server.base_handlers.get_server_root_dir") as grd:
                grd.return_value = "./"
                with mock.patch("aext_panels_server.base_handlers.NotebookBaseHandler._get_file_info") as m_gfi:
                    m_gfi.return_value = FileInfo(file_name="test-notebook.ipynb", file_size="120KB")
                    with mock.patch("aext_panels_server.base_handlers.PABaseHandler._log_notebook_data") as m_lbd:
                        self.fetch(
                            "/aext_panels_server/projects",
                            method="POST",
                            headers=headers,
                            body=urllib.parse.urlencode(form_data),
                        )
                        m_lbd.assert_awaited_once()
