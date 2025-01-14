from src.abc.sensor import Sensor
import pytest

def test_instantiation_fails():
    """
    Assert that the ABC errors if we try to instantiate it.
    """
    with pytest.raises(TypeError):
        s = Sensor()

