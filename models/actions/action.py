from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abstractmethod
    def undo(self, *args, **kwargs):
        pass