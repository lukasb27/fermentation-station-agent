from fermentation_station.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_last_action():
    response = client.get("/last_action")
    last_action = response.json().get("last_known_action")
    assert response.status_code == 200
    assert last_action
    assert response.json() == {"last_known_action": last_action}

    