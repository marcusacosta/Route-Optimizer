import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_optimize_endpoint_status_and_schema(client):
    payload = {
        "origin": [37.0, -122.0],
        "destinations": [[37.1, -122.1]],
        "time_of_day": 12,
        "traffic_level": 1
    }
    resp = client.post("/optimize", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    # must have both keys
    assert "optimized_route" in data
    assert "estimated_time" in data
    # types
    assert isinstance(data["optimized_route"], list)
    assert isinstance(data["estimated_time"], (int, float))
