import time
from utils.abstract_class import AbstractClass


class AbstractService(AbstractClass):
    def __init__(self):
        super().__init__(AbstractService)

    @AbstractClass.abstract_method
    def execute(self): ...

    def run_routine(self, routine, sleep=1):
        routine_iterator = routine()

        while True:
            try:
                value = next(routine_iterator)

            except StopIteration:
                break

            if value is not None and not isinstance(value, bool):
                raise Exception("Valor retornado da rotina é inválido")

            if value is False or value is None:
                time.sleep(sleep)

                continue

            if value is True:
                time.sleep(sleep)

                break
