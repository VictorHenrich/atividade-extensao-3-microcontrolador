from utils.abstract_class import AbstractClass


class AbstractService(AbstractClass):
    def __init__(self):
        super().__init__(AbstractService)

    @AbstractClass.abstract_method
    def execute(self): ...
