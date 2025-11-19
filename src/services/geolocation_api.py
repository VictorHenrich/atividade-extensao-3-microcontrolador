import urequests
from core.settings import LOCATION_SERVICE_URL
from core.abstract_service import AbstractService
from utils.datetime import DateTime


class GeolocationApiService(AbstractService):
    def execute(self):
        with urequests.get(LOCATION_SERVICE_URL) as response:
            if response.status_code >= 400:
                raise Exception(
                    f"Falha ao capturar dados de localização na API Geolocalização."
                )

            data = response.json()

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
