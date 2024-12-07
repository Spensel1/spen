import os
from pathlib import Path
from unittest import mock

import httpx
import pytest
from aext_panels_server.api import PythonAnywhereAPI
from aext_panels_server.const import AppStatus
from aext_panels_server.schemas import (
    AppVersion,
    MetaResponse,
    PAProjectInfo,
    ProjectInfoData,
    RequestError,
    ServiceResponse,
    VersioningData,
)
from aext_panels_server.services.project import project_service
from aext_panels_server.utils import get_utc_timestamp, get_vdate


@pytest.fixture(autouse=True, scope="session")
def setup_env_vars():
    os.environ["JUPYTERHUB_USER"] = "85c16f17-16e5-4a13-9009-9d9a486b8ebc"
    os.environ["API_TOKEN"] = "123456789"
    os.environ["NUCLEUS_CLOUDFLARE_CLIENT_ID"] = "nucleus-id"
    os.environ["NUCLEUS_CLOUDFLARE_CLIENT_SECRET"] = "nucleus-secret"


@pytest.fixture
def project_name():
    return "dummy-project_name"


@pytest.fixture
def project_description():
    return "Dummy project description"


@pytest.fixture
def project_versions():
    return [
        AppVersion(
            id="0955a586-9358-4628-b69e-58133834ecba",
            version="2023.1.1",
            created_at=str(get_utc_timestamp()),
            updated_at=str(get_utc_timestamp()),
            last_published_at=None,
        ),
        AppVersion(
            id="0955a586-9358-4628-b69e-58133834ecbb",
            version="2023.1.2",
            created_at=str(get_utc_timestamp()),
            updated_at=str(get_utc_timestamp()),
            last_published_at=None,
        ),
        AppVersion(
            id="0955a586-9358-4628-b69e-58133834ecbc",
            version="2023.1.2",
            created_at=str(get_utc_timestamp()),
            updated_at=str(get_utc_timestamp()),
            last_published_at=None,
        ),
    ]


@pytest.fixture
def project_environment():
    return "base"


@pytest.fixture
def project_id():
    return "c9bc616e-ca19-4983-ba1c-7ae0c6f8c190"


@pytest.fixture
def project_path():
    return "/home/user"


@pytest.fixture
def last_published_at():
    return str(get_utc_timestamp())


@pytest.fixture
def notebook_file_name():
    return "my_pretty_nb.ipynb"


@pytest.fixture
def notebook_file_size():
    return "747 Bytes"


@pytest.fixture
def project_info(
    project_versions,
    project_path,
    project_description,
    project_name,
    project_environment,
    project_id,
    last_published_at,
    notebook_file_name,
    notebook_file_size,
):
    return {
        "versions": project_versions,
        "description": project_description,
        "title": project_name,
        "path": project_path,
        "environment": project_environment,
        "project_id": project_id,
        "last_published_at": last_published_at,
        "notebook_file_name": notebook_file_name,
        "notebook_file_size": notebook_file_size,
    }


@pytest.fixture
def project_domains():
    return []


@pytest.fixture
def project_info_data(project_info, project_domains):
    return ProjectInfoData(
        title=project_info["title"],
        project_id=project_info["project_id"],
        description=project_info["description"],
        versioning=VersioningData(
            next_version=project_service._create_or_get_version(get_vdate(), PAProjectInfo(**project_info)),
            current_version=project_info["versions"][-1].version,
            all_versions=project_info["versions"],
        ),
        environment=project_info["environment"],
        notebook_file_name="my_pretty_nb.",
        notebook_file_size=project_info["notebook_file_size"],
        permission="public",
        last_published_at=project_info["last_published_at"],
        status=AppStatus.INACTIVE.value,
        domains=project_domains,
    )


@pytest.fixture
def _status_code():
    return 200


@pytest.fixture
def _json_resp():
    return {}


@pytest.fixture
def _binary_file_resp():
    return b"1234567890"


@pytest.fixture
def api_response(_status_code, _json_resp):
    return httpx.Response(status_code=_status_code, json=_json_resp)


@pytest.fixture
def bin_api_response(_status_code, _binary_file_resp):
    return httpx.Response(status_code=_status_code, content=_binary_file_resp)


@pytest.fixture()
def mock_python_anywhere_api(api_response):
    with mock.patch("aext_panels_server.api.PythonAnywhereAPI._simple_request") as m:
        m.return_value = api_response
        yield m


@pytest.fixture()
def mock_python_anywhere_api_bin(bin_api_response):
    with mock.patch("aext_panels_server.api.PythonAnywhereAPI._simple_request") as m:
        m.return_value = bin_api_response
        yield m


@pytest.fixture(scope="module")
def python_anywhere_api():
    return PythonAnywhereAPI()


@pytest.fixture
def project_index_response():
    return {
        "92a916ea-f0c6-49d6-bd75-16ab2244f134": {
            "webapp_id": 1,
            "title": "My Notebook 1",
        },
        "997c2ec0-9601-4729-a136-b855b88bc30f": {
            "webapp_id": None,
            "title": "My Notebook 2",
        },
    }


@pytest.fixture()
def mock_get_project_index(project_index_response):
    with mock.patch("aext_panels_server.services.project_index.ProjectIndexService.get_project_index") as m:
        m.return_value = ServiceResponse(
            meta=MetaResponse(error=RequestError(status=False)),
            content=project_index_response,
        )
        yield m


@pytest.fixture
def mock_project_index_save():
    with mock.patch("aext_panels_server.services.project_index.ProjectIndexService.save") as m:
        m.return_value = ServiceResponse(meta=MetaResponse(error=RequestError(status=False)), content={})
        yield m


@pytest.fixture()
def mock_services_deployment_status_is_live_enabled():
    with mock.patch("aext_panels_server.services.deployment_status.DeploymentStatus._is_live") as m:
        m.return_value = True
        yield m


@pytest.fixture()
def mock_services_deployment_status_is_live_not_enabled():
    with mock.patch("aext_panels_server.services.deployment_status.DeploymentStatus._is_live") as m:
        m.return_value = False
        yield m


@pytest.fixture
def project_error_log_response():
    with open(f"{Path.cwd()}/tests/assets/error.log", "r") as log_file:
        httpx_response = httpx.Response(200, text=log_file.read())
    return httpx_response


@pytest.fixture
def project_access_log_response():
    with open(f"{Path.cwd()}/tests/assets/access.log", "r") as log_file:
        httpx_response = httpx.Response(200, text=log_file.read())
    return httpx_response
