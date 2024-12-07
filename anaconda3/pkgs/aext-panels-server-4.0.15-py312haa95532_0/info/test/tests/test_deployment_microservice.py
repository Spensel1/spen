from unittest import mock
from uuid import uuid4

import httpx
import pytest
from aext_panels_server.api import project_deployment_ms_api
from aext_panels_server.api_v2 import project_deployment_ms_api_v2
from aext_panels_server.exceptions import CantUpdateProject
from aext_panels_server.request_schemas.notebook_projects_microservice import (
    UpdateProject,
)
from aext_panels_server.services.deployment_microservice import (
    project_microservice_service,
)
from tornado.httputil import HTTPServerRequest

from aext_shared.handler import UserAccessCredentials


@pytest.fixture
def project_id():
    return str(uuid4())


@pytest.fixture
def mock_ms_api_upload_project_archive():
    with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI.upload_project_archive") as m:
        m.return_value = httpx.Response(status_code=200)
        yield m


@pytest.fixture
def mock_start_app():
    with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI.start_app") as m:
        m.return_value = httpx.Response(
            status_code=200,
            content='{"domains": [{"name": "app.domain.name", "enabled": true}], "webapp_id": 123, "id": "id"}',
        )
        yield m


@pytest.fixture
def mock_ms_api_download_files():
    with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI.download_files") as m:
        m.return_value = httpx.Response(
            status_code=200, headers={"content-type": "application/json"}, content='{"archive": 123}'
        )
        yield m


@pytest.fixture
def mock_ms_api_update_project(project_id):
    with mock.patch("aext_panels_server.api.ProjectDeploymentMicroserviceAPI.update_project") as m:
        m.return_value = httpx.Response(
            status_code=200,
            json={
                "id": project_id,
                "title": "Foo",
                "versioning": {
                    "current_version": "2023.08.1",
                    "next_version": "2023.08.2",
                    "all_versions": ["2023.08.1"],
                },
                "notebook_file_name": "file.ipynb",
                "notebook_file_size": "120 Kbytes",
                "permission": "public",
                "environment": "env",
                "description": "New description",
                "last_published_at": None,
                "domains": [],
                "status": "inactive",
            },
        )
        yield m


async def test_update_project(mock_ms_api_upload_project_archive, mock_ms_api_update_project, project_id):
    request_data = UpdateProject(title="New Title", description="New description")
    archive_content = b"ARCHIVE-CONTENT"
    response = await project_microservice_service.update_project(project_id, request_data, archive_content)

    assert response.project_id == project_id
    mock_ms_api_update_project.assert_awaited_once()
    mock_ms_api_upload_project_archive.assert_awaited_once()


async def test_update_project_should_fail_if_upload_fails(
    mock_ms_api_upload_project_archive, mock_ms_api_update_project, project_id
):
    mock_ms_api_upload_project_archive.return_value = httpx.Response(status_code=400)
    request_data = UpdateProject(title="New Title", description="New description")
    archive_content = b"ARCHIVE-CONTENT"
    with pytest.raises(CantUpdateProject):
        await project_microservice_service.update_project(project_id, request_data, archive_content)


async def test_access_credentials_context_manager():
    user_creds = UserAccessCredentials(
        access_token="user-access-token",
        new_access_token="user-new-access-token",
        api_key="user-api-key",
        username="username",
    )
    async with project_microservice_service.access_credentials(user_creds):
        assert project_deployment_ms_api.anaconda_cloud_access_token == "user-access-token"
        assert project_deployment_ms_api_v2.anaconda_cloud_access_token == "user-access-token"
        assert project_deployment_ms_api.anaconda_cloud_username == "username"
        assert project_deployment_ms_api_v2.anaconda_cloud_username == "username"

    assert project_deployment_ms_api.anaconda_cloud_access_token is None
    assert project_deployment_ms_api_v2.anaconda_cloud_access_token is None


async def test_incoming_request_context_manager():
    request = HTTPServerRequest()
    async with project_microservice_service.incoming_request(request):
        assert project_deployment_ms_api.incoming_request == request
        assert project_deployment_ms_api_v2.incoming_request == request

    assert project_deployment_ms_api.incoming_request is None
    assert project_deployment_ms_api_v2.incoming_request is None


async def test_download_project_files(mock_ms_api_download_files):
    response = await project_microservice_service.download_project_files("project-id", "2023.01.1", api_version="v1")
    assert response.meta.error.status is False
    assert response.content == {"archive": 123}


async def test_start_app(mock_start_app):
    response = await project_microservice_service.start_app("app.domain.name", "user-id")
    assert response.meta.error.status is False
