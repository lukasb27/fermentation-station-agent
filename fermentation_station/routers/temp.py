from fastapi import APIRouter, Depends

from fermentation_station.abcs.sensor import Sensor
from fermentation_station.dependencies import get_temp_sensor

router = APIRouter()


@router.get("/temp")
async def get_temp(temp_sensor: Sensor = Depends(get_temp_sensor)):
    return {"temp": temp_sensor.get_value()}
