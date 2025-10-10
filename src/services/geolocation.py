from machine import UART
from libs.micropyGPS import MicropyGPS
from core.abstract_service import AbstractService
from core.settings import GPS_TX_PIN, GPS_RX_PIN
from utils.logging import Logging
from utils.datetime import DateTime


class GeolocationService(AbstractService):
    def __init__(self, tx_pin=GPS_TX_PIN, rx_pin=GPS_RX_PIN):
        self.__uart_pin = UART(2, baudrate=9600, tx=tx_pin, rx=rx_pin)

        self.__gps = MicropyGPS(location_formatting="dd")

        super().__init__()

    def __read_data_from_uart(self):
        if not self.__uart_pin.any():
            Logging.warning("Nenhum dado vindo da conexão UART")

            return

        return self.__uart_pin.readline()

    def __capture_geolocation_data(self, data):
        self.__gps.update(data)

        Logging.info(f"Dados vindos do GPS: {data}")

        if not self.__gps.valid:
            Logging.error("Os dados vindo do GPS são inválidos.")

            return

        geolocation_data = {
            "latitude": self.__gps.latitude[0],
            "longitude": self.__gps.longitude[0],
            "altitude": self.__gps.altitude,
            "speed": self.__gps.speed,
            "timestamp": str(DateTime.get_current_datetime()),
        }

        Logging.info(f"Dados Geolocalização: {geolocation_data}")

        return geolocation_data

    def execute(self):
        data = self.__read_data_from_uart()

        if not data:
            return

        return self.__capture_geolocation_data(data)
