import json

import pytest
from aext_panels_server.handlers_helpers import create_response


@pytest.mark.parametrize("status", [True, False])
def test_create_response_with_json_response(status):
    response = create_response(status=status, message="Message", content="Content", json_response=True)
    response = json.loads(response)
    assert response["content"] == "Content"
    assert response["meta"]["error"]["message"] == "Message"
    assert response["meta"]["error"]["status"] == status


@pytest.mark.parametrize("status", [True, False])
def test_create_response_with_no_json_response(status):
    response = create_response(status=status, message="Message", content="Content", json_response=False)
    assert response.content == "Content"
    assert response.meta.error.message == "Message"
    assert response.meta.error.status == status
