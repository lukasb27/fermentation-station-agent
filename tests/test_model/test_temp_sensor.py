from src.models.temp_sensor import TempSensor
import pytest

@pytest.fixture()
def temp_sensor():
    yield TempSensor()

def test_instatiates():
    assert TempSensor()

def test_get_value(temp_sensor):
    assert type(temp_sensor.get_value()) is int 
