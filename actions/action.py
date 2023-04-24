from abc import ABC, abstractmethod

from utils.initialize_project import initialize_project

class Action(ABC):
    
    @abstractmethod
    def get_name(self):
        return self.name 
