from io import BytesIO

import pytest
from aext_panels_server.schemas import (
    MetaResponse,
    PAProjectInfo,
    ProjectInfoData,
    RequestError,
    ServiceResponse,
    VersioningData,
)


def test_pa_project_info_to_bytes_io():
    project_info = PAProjectInfo(
        title="Project",
        project_id="id",
        notebook_file_name="filename",
        notebook_file_size="filesize",
        environment="environment",
        path="path",
    )

    assert type(project_info.to_bytes_io()) == BytesIO


@pytest.mark.parametrize("status, expected", [("", False), ("published", True)])
def test_project_info_data_is_active(status, expected):
    projeect_info_data = ProjectInfoData(
        title="title",
        project_id="project_id",
        versioning=VersioningData(next_version="2023.1.1"),
        notebook_file_name="filename",
        notebook_file_size="filesize",
        environment="environment",
        permission="permission",
        status=status,
    )
    assert projeect_info_data.is_active() == expected


@pytest.mark.parametrize("status, expected", [(True, False), (False, True)])
def test_service_response_has_failed_has_succeeded(status, expected):
    service_response = ServiceResponse(
        meta=MetaResponse(
            error=RequestError(status=status),
        ),
        content="",
    )
    has_failed_expected = not expected
    assert service_response.has_succeeded() == expected
    assert service_response.has_failed() == has_failed_expected


def test_service_response_set_error_message():
    service_response = ServiceResponse(
        meta=MetaResponse(
            error=RequestError(status=True),
        ),
        content="",
    )
    assert service_response.get_error_message() == ""
    service_response.set_error_message("error")
    assert service_response.get_error_message() == "error"


def test_service_response_set_error_status():
    service_response = ServiceResponse(
        meta=MetaResponse(
            error=RequestError(status=True),
        ),
        content="",
    )
    assert service_response.has_failed()
    service_response.set_error_status(False)
    assert service_response.has_succeeded()
