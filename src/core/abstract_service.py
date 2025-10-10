from utils.abstract_class import AbstractClass


class AbstractService(AbstractClass):
    def __init__(self):
        super().__init__(AbstractService)

    @AbstractClass.abstract_method
    def execute(self): ...

    def perform_loop(self):
        while True:
            self.execute()
