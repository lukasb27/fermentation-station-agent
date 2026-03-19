from fermentation_station.dependencies import get_temp_sensor


def test_get_temp_sensor_returns_dev_temp_sensor(monkeypatch):
    """ 
    The temp sensor factory should return the dev temp sensor 
    if ENVIRONMENT env var is set to dev 
    """
    from fermentation_station.services.temp_sensor import DevTempSensor
    monkeypatch.setenv("ENVIRONMENT", "dev")
    assert isinstance(get_temp_sensor(), DevTempSensor)

def test_get_temp_sensor_returns_prod_temp_sensor(monkeypatch):
    """ 
    The temp sensor factory should return the prod temp sensor 
    if ENVIRONMENT env var is set to prod 
    """
    from fermentation_station.services.temp_sensor import TempSensor
    monkeypatch.setenv("ENVIRONMENT", "prod")
    assert isinstance(get_temp_sensor(), TempSensor)

def test_get_temp_sensor_returns_dev_temp_sensor_default(monkeypatch):
    """ The temp sensor factory should return the dev temp sensor by default """
    from fermentation_station.services.temp_sensor import DevTempSensor
    monkeypatch.setenv("ENVIRONMENT", "defaulting")
    assert isinstance(get_temp_sensor(), DevTempSensor)

def test_get_temp_sensor_returns_dev_temp_sensor_no_env_var():
    """ The temp sensor factory should return the dev temp sensor if the env var doesnt exist """
    from fermentation_station.services.temp_sensor import DevTempSensor
    assert isinstance(get_temp_sensor(), DevTempSensor)