class AbstractClass:
    __default_error_message_in_constructor__ = (
        "It is not possible to instantiate the AbstractSocketConnection class directly"
    )

    __default_error_message_in_method__ = "Method was not implemented!"

    def __init__(self, class_):
        if type(self) is class_:
            raise NotImplementedError(
                AbstractClass.__default_error_message_in_constructor__
            )

    @classmethod
    def abstract_method(cls, function):
        def wrapper(*args, **kwargs):
            raise NotImplementedError(cls.__default_error_message_in_method__)

        return wrapper
