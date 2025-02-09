from abc import ABC, abstractmethod


class Graphic(ABC):
    @abstractmethod
    def run(self):
        pass
