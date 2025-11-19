from utils.abstract_class import AbstractClass


class AbstractApiIntegration(AbstractClass):
    def __init__(self, base_url):
        self.__base_url = base_url

    @property
    def headers(self):
        pass
