import pytest
import requests


@pytest.mark.api
def test_json_placeholder_posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
