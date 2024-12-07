import zipfile
from io import BytesIO
from unittest import mock

import pytest
import yaml
from aext_panels_server.api import project_deployment_ms_api
from aext_panels_server.exceptions import NbconvertNotInstalled, PanelNotInstalled
from aext_panels_server.schemas import FileInfo, PAProjectInfo
from aext_panels_server.services.project import project_service
from aext_panels_server.utils import clean_notebook, get_relative_file_path

from .fixtures import get_file_full_path


@pytest.fixture
def mocked_conda_list():
    return [
        {
            "base_url": "https://conda.anaconda.org/pypi",
            "build_number": 0,
            "build_string": "pypi_0",
            "channel": "pypi",
            "dist_name": "panel-1.0.4-pypi_0",
            "name": "panel",
            "platform": "pypi",
            "version": "1.0.4",
        },
        {
            "base_url": "https://conda.anaconda.org/pypi",
            "build_number": 0,
            "build_string": "pypi_0",
            "channel": "pypi",
            "dist_name": "nbconvert-0.0.4-pypi_0",
            "name": "nbconvert",
            "platform": "pypi",
            "version": "0.0.4",
        },
    ]


@pytest.fixture
def mock_conda_list(mocked_conda_list):
    with mock.patch("aext_panels_server.api.CondaAPI.list") as m:
        m.return_value = mocked_conda_list
        yield m


@pytest.mark.parametrize(
    "_status_code, _json_resp",
    [
        (
            200,
            {
                "versions": ["2023.1.1", "2023.1.2"],
                "description": "dummy",
                "title": "dummy-name",
                "path": "/home/user",
            },
        )
    ],
)
async def test_create_project_info_should_return_success(
    mock_python_anywhere_api,
    python_anywhere_api,
    _json_resp,
):
    notebook_file_info = FileInfo(
        file_name=get_file_full_path("assets/test-notebook.ipynb"),
        file_size="926 Bytes",
    )

    project_info = await project_service.create_project_info(
        title="dummy-project",
        version="2023.3.1",
        description="My new description",  # Modifying the description
        notebook_file_info=notebook_file_info,
        environment="base",
    )

    assert project_info.description != _json_resp["description"]
    assert len(project_info.versions) < len(_json_resp["versions"])


@pytest.mark.parametrize(
    "_status_code, _json_resp",
    [
        (
            200,
            {
                "title": "dummy-project",
                "project_id": "ad80abf2-9767-45bf-8c29-ec9699f2474e",
                "notebook_file_name": get_relative_file_path(get_file_full_path("assets/test-notebook.ipynb")),
                "notebook_file_size": "926 Bytes",
                "environment": "base",
                "path": ".projects/ad80abf2-9767-45bf-8c29-ec9699f2474e/project_info.json",
                "description": "My new description",
                "last_published_at": "",
                "versions": ["2023.3.1"],
            },
        )
    ],
)
async def test_get_project_info_should_return_successful(mock_python_anywhere_api, python_anywhere_api):
    notebook_file_info = FileInfo(
        file_name=get_file_full_path("assets/test-notebook.ipynb"),
        file_size="926 Bytes",
    )

    project_info = await project_service.create_project_info(
        title="dummy-project",
        version="2023.3.1",
        description="My new description",  # Modifying the description
        notebook_file_info=notebook_file_info,
        environment="base",
    )

    response = await project_service.get_project_info(
        api=python_anywhere_api,
        project_id=project_info.project_id,
    )
    assert project_info.title == response.title
    assert project_info.versions == response.versions
    assert project_info.description == response.description
    assert project_info.notebook_file_name == response.notebook_file_name
    assert project_info.notebook_file_size == response.notebook_file_size
    assert project_info.environment == response.environment


async def test_generate_zip_file(
    mock_python_anywhere_api,
    python_anywhere_api,
    _json_resp,
    mock_conda_list,
):
    project_name = "dummy-project"
    version = "2022.04.01"
    notebook = "test-notebook.ipynb"
    nb_path = get_file_full_path(f"assets/{notebook}")
    project_zip = await project_service.generate_zip_file("anaconda-user", project_name, version, "base", nb_path)
    assert isinstance(project_zip, BytesIO)
    files = {}
    with zipfile.ZipFile(project_zip) as zip_obj:
        for zipinfo in zip_obj.infolist():
            with zip_obj.open(zipinfo) as f:
                files[zipinfo.filename] = f.read()
    proj_yaml_file = f"{project_name}-{version}/conda-project.yaml"
    assert proj_yaml_file in files
    proj_yaml = yaml.load(files[proj_yaml_file], yaml.SafeLoader)
    assert proj_yaml == {
        "name": project_name,
        "maintainers": ["anaconda-user"],
        "platforms": ["linux-64"],
        "environments": {"default": ["environment.yaml"]},
        "commands": {"serve": {"cmd": f"panel serve {notebook}"}},
    }
    env_file = f"{project_name}-{version}/environment.yaml"
    assert env_file in files
    nb_file = f"{project_name}-{version}/{notebook}"
    assert nb_file in files
    with open(nb_path, "r") as f:
        assert files[nb_file].decode("utf-8") == clean_notebook(f.read())


@pytest.mark.parametrize(
    "mocked_conda_list",
    [
        [
            {
                "base_url": "https://conda.anaconda.org/pypi",
                "build_number": 0,
                "build_string": "pypi_0",
                "channel": "pypi",
                "dist_name": "notpanel-1.0.4-pypi_0",
                "name": "notpanel",
                "platform": "pypi",
                "version": "1.0.4",
            }
        ]
    ],
)
async def test_generate_zip_file_should_contain_panels(
    mock_python_anywhere_api,
    python_anywhere_api,
    _json_resp,
    mock_conda_list,
):
    project_name = "dummy-project"
    version = "2022.04.01"
    notebook = "test-notebook.ipynb"
    nb_path = get_file_full_path(f"assets/{notebook}")
    with pytest.raises(PanelNotInstalled):
        await project_service.generate_zip_file("anaconda-user", project_name, version, "base", nb_path)


@pytest.mark.parametrize(
    "mocked_conda_list",
    [
        [
            {
                "base_url": "https://conda.anaconda.org/pypi",
                "build_number": 0,
                "build_string": "pypi_0",
                "channel": "pypi",
                "dist_name": "panel-1.0.4-pypi_0",
                "name": "panel",
                "platform": "pypi",
                "version": "1.0.4",
            }
        ]
    ],
)
async def test_generate_zip_file_should_have_nbconvert(
    mock_python_anywhere_api,
    python_anywhere_api,
    _json_resp,
    mock_conda_list,
    mocked_conda_list,
):
    project_name = "dummy-project"
    version = "2022.04.01"
    notebook = "test-notebook.ipynb"
    nb_path = get_file_full_path(f"assets/{notebook}")
    with pytest.raises(NbconvertNotInstalled):
        await project_service.generate_zip_file("anaconda-user", project_name, version, "base", nb_path)


async def test_generate_files(project_info, mock_conda_list):
    project_info["notebook_file_name"] = get_file_full_path("assets/test-notebook.ipynb")
    project_info["notebook_file_size"] = "926 Bytes"

    project_content = await project_service.generate_files(
        "anaconda-user",
        project_info["title"],
        project_info["versions"][-1],
        PAProjectInfo(**project_info),
        project_info["environment"],
        get_file_full_path("assets/test-notebook.ipynb"),
    )

    assert isinstance(project_content.project_info_content, BytesIO)
    assert isinstance(project_content.archive_content, BytesIO)


async def test_project_versions():
    valid_versions = ["2023.04.1", "2023.04.12", "2023.05.31", "2023.05.212"]
    invalid_versions = ["2023.04.01", "2023.04", "2023.05.031", ""]

    for version in valid_versions:
        assert project_service.is_valid_version(version) is True

    for version in invalid_versions:
        assert project_service.is_valid_version(version) is False


def test_set_anaconda_cloud_access_token():
    project_deployment_ms_api.set_anaconda_cloud_access_token("user-access-token")
    assert project_deployment_ms_api.anaconda_cloud_access_token == "user-access-token"
