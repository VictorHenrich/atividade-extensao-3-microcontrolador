from services.root import RootService
from services.geolocation_api import GeolocationApiService

if __name__ == "__main__":
    geolocation_service = GeolocationApiService()

    root_service = RootService(geolocation_service)

    root_service.execute()
