import os
from unittest.mock import patch

import jupyterlab
import jupyterlab_server
import pytest

from aext_shared.config import get_config


@pytest.fixture
def default_config():
    return {
        "heap": {"clientId": "758475466"},
        "datadog": {"clientToken": "pub2b6467ca1f0ee597585d8a8bf43d523f", "service": "nb.anaconda.cloud"},
        "featureFlag": {
            "clientId": "6408b2b7e550011343183538",
            "overrides": {},
        },
        "cloud": {
            "url": "https://anaconda.cloud/api",
            "staticContent": "https://static.anaconda.cloud/shared",
        },
        "org": {
            "url": "https://notebooks.anaconda.org",
        },
        "notebooks": {"url": "https://nb.anaconda.cloud"},
        "environment": "development",
        "jupyterlab": {"server": jupyterlab_server.__version__, "client": jupyterlab.__version__},
        "assistant": {
            "environmentType": "cloud-notebooks-prod",
            "apiUrl": "https://assistant.anaconda.cloud",
        },
    }


@patch.dict(os.environ, {}, clear=True)
def test_get_default_config(default_config):
    assert get_config() == default_config


@patch.dict(
    os.environ,
    {
        "PYTHONANYWHERE_SITE": "https://nb.anaconda.cloud",
        "ANACONDA_NOTEBOOKS_URL": "https://nb.anaconda.cloud",
    },
    clear=True,
)
def test_get_config_with_production_environment(default_config):
    config = get_config()
    assert config["environment"] == "production"


@patch.dict(
    os.environ,
    {"DEBUG_AEXT_SHARED_LOCAL": "true"},
    clear=True,
)
def test_local_config(default_config):
    config = get_config()
    expected = default_config
    expected["heap"]["clientId"] = None
    expected["datadog"]["clientToken"] = None
    expected["datadog"]["service"] = None
    expected["featureFlag"]["clientId"] = None
    expected["featureFlag"]["overrides"] = {
        "monorepo-assistant": True,
        "monorepo-panel": True,
        "panel-sign-out-jupyterlab": True,
        "share-notebook-use-projects-v2": True,
        "sharing-show-preview": True,
        "monorepo-share-notebooks": True,
        "monorepo-panel-show-publish-button": False,
    }
    expected["environment"] = "local"
    expected["assistant"] = {
        "environmentType": "local-notebooks-prod",
        "apiUrl": "https://assistant.anaconda.cloud",
    }
    assert config == expected
