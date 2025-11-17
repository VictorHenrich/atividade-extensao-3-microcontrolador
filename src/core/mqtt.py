from umqtt.simple import MQTTClient
import _thread as threading
import json
import time

from core.settings import MQTT_HOST, MQTT_PORT, MQTT_CLIENT_ID
from utils.logging import Logging
from utils.abstract_class import AbstractClass


class MQTTHandler(AbstractClass):
    __topic__ = ""

    def __init__(self, mqtt_reference):
        self.__mqtt_reference = mqtt_reference

    @property
    def mqtt_reference(self):
        return self.__mqtt_reference

    @AbstractClass.abstract_method
    def handle(self, data): ...

    def serialize(self, message):
        return message.decode()


class MQTT(MQTTClient):
    def __init__(self, host=MQTT_HOST, port=MQTT_PORT, handler_classes=[]):
        client_id = f"{MQTT_CLIENT_ID}_{time.time()}"

        super().__init__(client_id, host, port)

        self.__handler_classes = handler_classes

    def __handle_lopping(self):
        while True:
            try:
                self.wait_msg()

            except Exception as error:
                Logging.error(f"MQTT Error: {error}")

    def __subscribe_and_initialize_handlers(self):
        if not self.__handler_classes:
            return

        self.set_callback(self.__get_message_callback())

        for handler_class in self.__handler_classes:
            self.subscribe(handler_class.__topic__.encode())

            threading.start_new_thread(self.__handle_lopping, ())

    def __get_message_callback(self):
        def callback(topic, message):
            topic_handled = topic.decode()

            for handler_class in self.__handler_classes:
                if handler_class.__topic__ == topic_handled:
                    handler_object = handler_class(self)

                    data = handler_object.serialize(message)

                    handler_object.handle(data)

        return callback

    def publish(self, topic, message):
        data = message

        if isinstance(data, dict):
            data = json.dumps(data)

        super().publish(topic, data)

    def start(self):
        self.connect()

        self.__subscribe_and_initialize_handlers()
