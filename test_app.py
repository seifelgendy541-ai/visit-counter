from app import app
import redis

def test_visits_return_count(mocker):
    mocker_test = mocker.patch("app.cache")
    mocker_test.incr.return_value = 7

    client_browser = app.test_client()
    client_visits = client_browser.get("/visits")

    assert client_visits.status_code == 200
    assert client_visits.text == "Visits: 7"


def test_when_redis_down(mocker):
    mocker_test = mocker.patch("app.cache")
    mocker_test.incr.side_effect = redis.exceptions.ConnectionError()

    client_browser = app.test_client()
    response = client_browser.get("/visits")

    assert response.status_code == 503 
    assert "unavailable" in response.text 
