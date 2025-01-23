from abc import ABC, abstractmethod

from src.abcs.sensor import Sensor


class Controller(ABC):
    """Controller Abstract Base Class"""

    @abstractmethod
    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    @abstractmethod
    def perform_action(self):
        pass

    @abstractmethod
    def _heat(self):
        pass

    @abstractmethod
    def _cool(self):
        pass
