import urequests
from core.settings import LOCATION_SERVICE_URL
from core.abstract_service import AbstractService
from utils.datetime import DateTime
from utils.logging import Logging


class GeolocationApiService(AbstractService):
    def execute(self):
        response = urequests.get(LOCATION_SERVICE_URL)

        Logging.info(
            f"Resposta da requisição: {LOCATION_SERVICE_URL}\n"
            f"STATUS_CODE={response.status_code}\n"
            f"CONTENT={response.text}"
        )

        if response.status_code >= 400:
            response.close()

            raise Exception(
                f"Falha ao capturar dados de localização na API Geolocalização."
            )

        data = response.json()

        response.close()

        return {
            "country": data["country"],
            "country_code": data["countryCode"],
            "region": data["region"],
            "region_name": data["regionName"],
            "city": data["city"],
            "zip": data["zip"],
            "latitude": data["lat"],
            "longitude": data["lon"],
            "timezone": data["timezone"],
            "timestamp": str(DateTime.get_current_datetime()),
        }
