from fermentation_station.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_temp():
    response = client.get("/temp")
    val = response.json().get('temp')
    assert response.status_code == 200
    assert type(val) is int
    assert response.json() == {'temp': val}