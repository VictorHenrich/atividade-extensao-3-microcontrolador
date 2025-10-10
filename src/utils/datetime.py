import time


class DateTime:
    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0):
        self.__year = year

        self.__month = month

        self.__day = day

        self.__hour = hour

        self.__minute = minute

        self.__second = second

        self.__microsecond = microsecond

    def __str__(self):
        return f"{self.__year}-{self.__month}-{self.__day} {self.__hour}:{self.__minute}:{self.__second}-{self.__microsecond}"

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def hour(self):
        return self.__hour

    @property
    def minute(self):
        return self.__minute

    @property
    def second(self):
        return self.__second

    @property
    def microsecond(self):
        return self.__microsecond

    @staticmethod
    def get_current_datetime():
        year, month, day, hour, minute, second, _, _ = time.localtime()  # type: ignore

        return DateTime(
            year=year, month=month, day=day, hour=hour, minute=minute, second=second
        )
