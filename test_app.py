from app import app,cache
import redis
import pytest

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


def test_visits_integration_real_redis():
    try: 
        cache.ping()
    except redis.exceptions.RedisError:
        pytest.skip("redis is not running")
    client_browser = app.test_client()
    first = client_browser.get("/visits").text
    second = client_browser.get("/visits").text
    first = first.split(": ")
    second = second.split(": ")
    before = int(first[1])
    after = int(second[1])
    assert after == before +1  
