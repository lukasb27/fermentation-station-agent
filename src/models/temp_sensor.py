from random import randint

from src.abcs.sensor import Sensor


class TempSensor(Sensor):
    """
    Class for getting the temp sensor data
    """

    def get_value(self) -> int:
        """Get value from the temperature sensor

        :return: return temperature data
        :rtype: int
        """

        return randint(0, 30)
