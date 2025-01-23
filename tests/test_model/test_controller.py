from src.models.controller import Controller
import pytest
from unittest.mock import MagicMock


    
@pytest.fixture()
def controller():
    yield Controller()

def get_mock_sensor(value: int):
    class MockSensor():
        def get_value(self):
            return 0
    sensor = MockSensor()
    sensor.get_value = MagicMock(return_value=value)

    return sensor

def test_instatiates():
    assert Controller()
    
def test_has_correct_class_values():
    c = Controller()
    assert c.sensor  

def test_logic_no_action():
    sensor = get_mock_sensor(19)
    c = Controller(sensor)
    assert c.perform_action() == {"status": "nothing needed"}

def test_logic_cooling():
    sensor = get_mock_sensor(24)
    c = Controller(sensor)
    assert c.perform_action() == {"status": "cooling"}

def test_logic_heating():
    sensor = get_mock_sensor(15)
    c = Controller(sensor)
    assert c.perform_action() == {"status": "heating"}