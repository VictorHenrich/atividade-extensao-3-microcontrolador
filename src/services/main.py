from core.abstract_service import AbstractService
from core.stream import StreamClient, AbstractStreamClientHandler
from services.geolocation import GeolocationService
from utils.logging import Logging
from utils.network import Network


class ClientHandler(AbstractStreamClientHandler):
    def on_receive(self, data):
        Logging.info(f"Recebendo dados do servidor: {data}")


class MainService(AbstractService):
    def __init__(self):
        self.__stream_client = StreamClient(ClientHandler)

        self.__geolocation_service = GeolocationService()

    def __connect_to_network(self):
        try:
            Network.connect_wifi()

        except Exception as error:
            Logging.error(f"Falha ao se conectar no wifi: {error}")

            return False

        else:
            if not Network.wifi_connected():
                Logging.warning("O Wifi ainda não foi conectado, aguarde um momento.")

                return False

            Logging.info("Wifi conectado com sucesso.")

            return True

    def __start_and_validate_stream_client(self):
        try:
            self.__stream_client.start()

        except Exception as error:
            Logging.error(f"Falha ao se conectar no servidor Socket: {error}")

            return False

        else:
            Logging.info("Servidor Socket conectado com sucesso.")

            return True

    def __send_data_to_socket_server(self):
        geolocation_data = self.__geolocation_service.execute()

        if not geolocation_data:
            return

        Logging.info("Disparando mensagem ao servidor.")

        self.__stream_client.send_data(geolocation_data)

    def execute(self):
        if not self.__connect_to_network():
            return

        if not self.__start_and_validate_stream_client():
            return

        self.__send_data_to_socket_server()
