from flaky_service import call_service
import pytest

def test_call_service_succeeds_when_service_up(mocker):
    mocker_test = mocker.patch("flaky_service.random.random")
    mocker_test.return_value = 0.9

    assert call_service() == "ok"

def test_call_service_raises_when_service_down(mocker):
    mocker_test = mocker.patch("flaky_service.random.random")
    mocker_test.return_value = 0.1

    with pytest.raises(ConnectionError):
        call_service()

