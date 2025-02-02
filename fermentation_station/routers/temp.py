from fastapi import APIRouter, Depends

from fermentation_station.models.temp_sensor import TempSensor

router = APIRouter()


def get_temp_sensor() -> TempSensor:
    return TempSensor()


@router.get("/temp")
async def get_temp(temp_sensor: TempSensor = Depends(get_temp_sensor)):
    return {"temp": temp_sensor.get_value()}
