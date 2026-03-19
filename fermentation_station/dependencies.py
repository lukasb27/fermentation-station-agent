import os

from fermentation_station.services.temp_sensor import TempSensor, DevTempSensor
from fermentation_station.abcs.sensor import Sensor


def get_temp_sensor() -> Sensor:
    if os.getenv("ENVIRONMENT", "dev") == "prod":
        return TempSensor()

    return DevTempSensor()
