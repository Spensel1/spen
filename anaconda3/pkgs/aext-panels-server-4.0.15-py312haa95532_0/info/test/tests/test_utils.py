import json
import os
from datetime import datetime
from unittest import mock

import pytest
import pytz
from aext_panels_server import utils
from aext_panels_server.const import PYTHONANYWHERE_PRODUCTION_SITE, Environment
from aext_panels_server.schemas import MetaResponse, RequestError, ServiceResponse

from .fixtures import get_file_full_path


@pytest.mark.parametrize(
    "PYTHONANYWHERE_SITE, is_staging", ((PYTHONANYWHERE_PRODUCTION_SITE, False), ("non-prod.anaconda.cloud", True))
)
def test_is_staging_env(PYTHONANYWHERE_SITE, is_staging):
    os.environ["PYTHONANYWHERE_SITE"] = PYTHONANYWHERE_SITE
    assert utils.is_staging_env() == is_staging


@pytest.mark.parametrize(
    "PYTHONANYWHERE_SITE, LOCAL_ENV, expected",
    (
        ("non-prod.anaconda.cloud", "", Environment.STAGING),
        (PYTHONANYWHERE_PRODUCTION_SITE, "", Environment.PRODUCTION),
        ("non-prod.anaconda.cloud", "1", Environment.LOCAL),
        ("", "", Environment.PRODUCTION),  # TOLBOX: NO PA ENVS AND NO LOCAL_ENV
    ),
)
def test_get_environment(PYTHONANYWHERE_SITE, LOCAL_ENV, expected):
    os.environ["PYTHONANYWHERE_SITE"] = PYTHONANYWHERE_SITE
    os.environ["LOCAL_ENV"] = LOCAL_ENV
    assert utils.get_environment() == expected


def test_to_json():
    response = ServiceResponse(
        meta=MetaResponse(error=RequestError(status=False)),
        content={},
    )
    json_response = utils.to_json(response)
    assert json_response == '{"meta": {"error": {"status": false, "message": ""}}, "content": {}}'


@pytest.mark.parametrize(
    "file_path, remove_extension, expected",
    (
        ("test.ipynb", True, "test"),
        ("test.ipynb", False, "test.ipynb"),
    ),
)
def test_extract_file_name(file_path, remove_extension, expected):
    assert utils.extract_file_name(file_path, remove_extension) == expected


async def test_run_concurrently():
    async def _coroutine():
        return True

    coros = {"testing_coroutine": _coroutine()}
    result = await utils.run_concurrently(coros)
    assert result == {"testing_coroutine": True}


def test_get_vdate():
    vdate = utils.get_vdate()
    assert vdate == f"{datetime.now().year}.{datetime.now().month:0>2}"


def test_to_snake_case():
    names = ["test", "test123", "testSnake", "CamelCaseIsCool"]
    expected_snake_names = ["test", "test123", "testsnake", "camelcaseiscool"]
    assert utils.to_snake_case(names) == expected_snake_names


def test_get_utc_timestamp():
    datetime_now = datetime(2024, 1, 23, 0, 0, 0, 0, pytz.UTC)
    with mock.patch("aext_panels_server.utils.datetime") as m:
        m.utcnow.return_value = datetime_now
        assert utils.get_utc_timestamp() == 1705968000


@pytest.mark.parametrize(
    "username, pythonanywhere_user, expected",
    (
        ("", "python-anywhere-username", "python-anywhere-username"),
        ("username", "", "username"),
        ("", "", "unknown"),
    ),
)
def test_get_username(username, pythonanywhere_user, expected):
    os.environ.pop("USERNAME", None)
    os.environ.pop("PYTHONANYWHERE_USER", None)
    if username:
        os.environ["USERNAME"] = username
    if pythonanywhere_user:
        os.environ["PYTHONANYWHERE_USER"] = pythonanywhere_user

    assert utils.get_username() == expected


@pytest.mark.parametrize("file_path, expected", (("/User/test/file.txt", "file.txt"), ("file.txt", "file.txt")))
def test_get_relative_file_path(file_path, expected):
    assert utils.get_relative_file_path(file_path) == expected


def test_notebook_clean_metadata():
    nb_filepath = get_file_full_path("assets/test-notebook.ipynb")
    with open(nb_filepath, "r", encoding="utf-8") as nbfile:
        nbdata = nbfile.read()
    clean_nb = utils.clean_notebook(nbdata)
    nb = json.loads(clean_nb)

    assert len(nb["cells"]) == 1
    cell = nb["cells"][0]
    assert cell["execution_count"] is None
    assert cell["metadata"] == {"panel-layout": {"width": 42, "height": 7}}
    assert "panel-cell-order" in nb["metadata"]
    assert nb["metadata"]["panel-cell-order"] == [cell["id"]]
