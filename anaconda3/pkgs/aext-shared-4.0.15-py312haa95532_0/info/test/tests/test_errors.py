import pytest

from aext_shared.errors import BackendError, BadRequest, UnknownError


@pytest.mark.parametrize(
    ["error", "status_code", "message"],
    [
        [BackendError(400, {"other": "data"}), 400, "BackendError 400: unknown"],
        [BackendError(500, {"reason": "nope"}), 500, "BackendError 500: nope"],
        [UnknownError({"reason": "nope"}), 500, "BackendError 500: nope"],
        [UnknownError({}), 500, "BackendError 500: unknown"],
        [BadRequest({}), 400, "BackendError 400: bad_request"],
        [BadRequest({"reason": "nope"}), 400, "BackendError 400: nope"],
    ],
)
def test_errors(error: BackendError, status_code, message):
    assert error.status_code == status_code
    assert str(error) == message
