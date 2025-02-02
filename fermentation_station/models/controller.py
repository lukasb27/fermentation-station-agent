from typing import Dict

from fermentation_station.abcs.controller import Controller
from fermentation_station.constants import MAX_TEMP, MIN_TEMP
from fermentation_station.models.temp_sensor import TempSensor


class Controller(Controller):
    """Controller Model"""

    def __init__(self, sensor: TempSensor = TempSensor()):
        """Constructor for controller class.

        :param sensor: sensor, used for getting values for the controller,
          defaults to TempSensor()
        :type sensor: TempSensor, optional
        """
        self.sensor = sensor

    def perform_action(self) -> Dict[str, str]:
        """
        Read the value of the sensor, perform an appropriate action
        based on that.

        :return: Dictionary with status and action.
        :rtype: Dict[str, str]
        """
        temp = self.sensor.get_value()
        if temp > MAX_TEMP:
            return self._cool()
        elif temp < MIN_TEMP:
            return self._heat()
        else:
            return {"status": "nothing needed"}

    def _heat(self) -> Dict[str, str]:
        """Heat the station.

        :return: Dictionary with heating status.
        :rtype: Dict[str, str]
        """
        return {"status": "heating"}

    def _cool(self) -> Dict[str, str]:
        """Cool the station.

        :return: Dictionary with heating status.
        :rtype: Dict[str, str]
        """
        return {"status": "cooling"}
