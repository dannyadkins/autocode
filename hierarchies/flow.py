from abc import ABC, abstractmethod

from utils.initialize_project import initialize_project

class Flow(ABC):
    @abstractmethod
    def run(self, src_folder, task):
        pass

    def prepare(self, src_folder):
        initialize_project(src_folder)

