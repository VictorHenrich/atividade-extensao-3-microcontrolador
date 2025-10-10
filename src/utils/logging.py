from .datetime import DateTime


class Logging:
    __error_level_text__ = "ERROR"

    __info_level_text__ = "INFO"

    __warning_level_text__ = "WARNING"

    __debug_level_text__ = "DEBUG"

    @staticmethod
    def __print_message(level, *messages):
        print(f"{level} - [{DateTime.get_current_datetime()}] {''.join(messages)}")

    @classmethod
    def info(cls, *messages):
        cls.__print_message(cls.__info_level_text__, *messages)

    @classmethod
    def debug(cls, *messages):
        cls.__print_message(cls.__debug_level_text__, *messages)

    @classmethod
    def warning(cls, *messages):
        cls.__print_message(cls.__warning_level_text__, *messages)

    @classmethod
    def error(cls, *messages):
        cls.__print_message(cls.__error_level_text__, *messages)
