from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def execute(self, task):
        pass

    def get_context(self):
        pass


