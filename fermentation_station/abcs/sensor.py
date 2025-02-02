from abc import ABC, abstractmethod


class Sensor(ABC):
    @abstractmethod
    def get_value(self) -> int:
        pass
