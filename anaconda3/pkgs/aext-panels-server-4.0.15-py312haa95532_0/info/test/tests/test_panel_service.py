from unittest import mock

import pytest
from aext_panels_server.schemas import (
    ListDeploymentsResponse,
    MetaResponse,
    PAProjectInfo,
    RequestError,
    ServiceResponse,
)
from aext_panels_server.services.panel import panel_service


@pytest.fixture
def project_id_1():
    return "30b9ffb6-fc28-4190-a032-9932c4299148"


@pytest.fixture
def project_id_2():
    return "368bec4f-3899-463d-8ab3-98843d026385"


@pytest.fixture
def project_id_3():
    return "7c48a61c-91f3-405a-800c-0911be9b7393"


@pytest.fixture
def webapp_id_1():
    return 1


@pytest.fixture
def webapp_id_2():
    return 2


@pytest.fixture
def list_deployments_response(webapp_id_1, webapp_id_2):
    content = ListDeploymentsResponse(
        deployments=[
            {
                "id": webapp_id_1,
                "user": "e761da58-732e-4943-af40-5d4caba41bfe",
                "command": "",
                "domains": [
                    {
                        "id": webapp_id_1,
                        "user": "e761da58-732e-4943-af40-5d4caba41bfe",
                        "domain_name": "gdipnixthvcu.nb.anaconda.cloud",
                        "enabled": True,
                        "webapp": webapp_id_1,
                    }
                ],
            },
            {
                "id": webapp_id_2,
                "user": "e761da58-732e-4943-af40-5d4caba41bfe",
                "command": "",
                "domains": [
                    {
                        "id": webapp_id_2,
                        "user": "e761da58-732e-4943-af40-5d4caba41bfe",
                        "domain_name": "jlvfhutudboo.nb.anaconda.cloud",
                        "enabled": True,
                        "webapp": webapp_id_2,
                    }
                ],
            },
        ]
    )
    return ServiceResponse(meta=MetaResponse(error=RequestError(status=False, message="")), content=content)


@pytest.fixture
def project_index_response(project_id_1, project_id_2, project_id_3, webapp_id_1, webapp_id_2):
    return {
        project_id_1: {"webapp_id": webapp_id_1, "title": "My Notebook #1"},
        project_id_2: {"webapp_id": webapp_id_2, "title": "My Notebook #2"},
        project_id_3: {"webapp_id": None, "title": "My Notebook #3"},
    }


@pytest.fixture
def mock_get_project_index(project_index_response):
    with mock.patch("aext_panels_server.services.project_index.ProjectIndexService.get_project_index") as m:
        m.return_value = ServiceResponse(
            meta=MetaResponse(error=RequestError(status=False)),
            content=project_index_response,
        )
        yield m


@pytest.fixture
def mock_get_project_info(python_anywhere_api, project_id_1, project_id_2, project_id_3):
    def args_based_return(*args, **kwargs):
        if args == (python_anywhere_api, project_id_1):
            return PAProjectInfo(
                title="My project #1",
                path="my-notebook-1.ipynb",
                notebook_file_name="my-notebook-1.ipynb",
                notebook_file_size="100 Bytes",
                environment="base",
                project_id=project_id_1,
                description="This is my project #1",
                versions=["2023.04.1"],
            )
        elif args == (python_anywhere_api, project_id_2):
            return PAProjectInfo(
                title="My project #2",
                path="my-notebook-2.ipynb",
                notebook_file_name="my-notebook-2.ipynb",
                notebook_file_size="200 Bytes",
                environment="base",
                project_id=project_id_2,
                description="This is my project #2",
                versions=["2023.04.1", "2023.04.2"],
            )
        elif args == (python_anywhere_api, project_id_3):
            return PAProjectInfo(
                title="My project #3",
                path="my-notebook-3.ipynb",
                notebook_file_name="my-notebook-3.ipynb",
                notebook_file_size="300 Bytes",
                environment="base",
                project_id=project_id_3,
                description="This is my project #3",
                versions=["2023.04.1", "2023.04.2", "2023.04.3"],
            )
        else:
            return Exception("exception occurred")

    with mock.patch("aext_panels_server.services.project.ProjectService.get_project_info") as m:
        m.side_effect = args_based_return
        yield m


@pytest.fixture
def mock_index_service_exists():
    with mock.patch("aext_panels_server.services.project_index.ProjectIndexService.exists") as m:
        m.return_value = True
        yield m


@pytest.fixture
def project_delete_response_content():
    return {}


@pytest.fixture
def project_delete_response_meta():
    return MetaResponse(error=RequestError(status=False, message=""))


@pytest.fixture
def project_delete_response(project_delete_response_meta, project_delete_response_content):
    return ServiceResponse(meta=project_delete_response_meta, content=project_delete_response_content)


@pytest.fixture
def deployment_delete_response_content():
    return {}


@pytest.fixture
def deployment_delete_response_meta():
    return MetaResponse(error=RequestError(status=False, message=""))


@pytest.fixture
def deployment_delete_response(deployment_delete_response_meta, deployment_delete_response_content):
    return ServiceResponse(meta=deployment_delete_response_meta, content=deployment_delete_response_content)


@pytest.fixture
def mock_project_delete(project_delete_response):
    with mock.patch("aext_panels_server.services.project.ProjectService.delete") as m:
        m.return_value = project_delete_response
        yield m


@pytest.fixture()
def mock_utils_call_api_error_log(project_error_log_response):
    with mock.patch("aext_panels_server.services.panel.call_api") as m:
        m.return_value = RequestError(status=False, message=""), project_error_log_response
        yield m


async def test_get_app_logs_should_return_successful_error_log_file(python_anywhere_api, mock_utils_call_api_error_log):
    domain = "great_anaconda.anacondaapps.com"
    response = await panel_service.get_app_log(python_anywhere_api, domain, "error_log")
    assert response.meta.error.status is False
    assert response.content != ""


@pytest.fixture()
def mock_utils_call_api_access_log(project_access_log_response):
    with mock.patch("aext_panels_server.services.panel.call_api") as m:
        m.return_value = RequestError(status=False, message=""), project_access_log_response
        yield m


async def test_get_app_logs_should_return_successful_access_log_file(
    python_anywhere_api, mock_utils_call_api_access_log
):
    domain = "great_anaconda.anacondaapps.com"
    response = await panel_service.get_app_log(python_anywhere_api, domain, "access_log")
    assert response.meta.error.status is False
    assert response.content != ""
