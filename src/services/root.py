import time
from core.abstract_service import AbstractService
from core.mqtt import MQTT
from core.settings import MQTT_GEOLOCATION_TOPIC
from utils.logging import Logging
from utils.network import Network


class RootService(AbstractService):
    def __init__(self, geolocation_service):
        self.__mqtt_client = MQTT()

        self.__geolocation_service = geolocation_service

    def __connect_to_network(self):
        try:
            Network.connect_wifi()

        except Exception as error:
            Logging.error(f"Falha ao se conectar no wifi: {error}")

            return False

        else:
            if not Network.wifi_connected():
                Logging.warning("O Wifi ainda não foi conectado, tentando novamente.")

                return False

            Logging.info("Wifi conectado com sucesso.")

            return True

    def __start_and_validate_mqtt_client(self):
        try:
            self.__mqtt_client.start()

        except Exception as error:
            Logging.error(f"Falha ao se conectar no servidor MQTT: {error}")

            return False

        else:
            Logging.info("Servidor MQTT conectado com sucesso.")

            return True

    def __send_data_to_socket_server(self):
        geolocation_data = self.__geolocation_service.execute()

        if not geolocation_data:
            return False

        Logging.info(f"Disparando mensagem ao servidor: {geolocation_data}")

        try:
            self.__mqtt_client.publish(MQTT_GEOLOCATION_TOPIC, geolocation_data)

        except Exception as error:
            Logging.error(f"Falha ao disparar mensagem ao servidor MQTT: {error}")

            return False

    def execute(self):
        Logging.info("...Iniciando serviço principal...")

        Logging.info("Conectando-se ao Wifi.")

        self.run_routine(self.__connect_to_network)

        Logging.info("Conectando-se ao servidor MQTT.")

        self.run_routine(self.__start_and_validate_mqtt_client)

        Logging.info("Abrindo comunicação com GPS.")

        self.run_routine(self.__send_data_to_socket_server)
