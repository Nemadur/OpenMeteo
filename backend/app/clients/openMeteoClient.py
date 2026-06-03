import openmeteo_requests
import requests_cache
import requests
from retry_requests import retry

# This client is responsible for all interactions with the Open-Meteo API, including geocoding and weather data retrieval. It uses caching and retries to optimize performance and reliability.
# The client provides two main methods: 
# geocode_city for converting city names to coordinates, 
# fetch_weather for retrieving weather data based on those coordinates and a specified date range. The weather data is returned in a format suitable for scoring by the ScoringService.

class OpenMeteoClient:
    def __init__(self):
        cache_session = requests_cache.CachedSession(
            ".cache",
            expire_after=3600
        )

        retry_session = retry(
            cache_session,
            retries=5,
            backoff_factor=0.2
        )

        self.client = openmeteo_requests.Client(session=retry_session)

    def geocode_city(self, city: str):
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        )

        data = response.json()

        if not data.get("results"):
            raise ValueError(f"City not found: {city}")

        result = data["results"][0]

        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"]
        }

    def fetch_weather(self, latitude: float, longitude: float, start_date: str,
    end_date: str):
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "temperature_2m",
                "wind_speed_10m",
                "relative_humidity_2m",
                "cloud_cover"
            ],
            "start_date": start_date,
            "end_date": end_date
        }

        responses = self.client.weather_api(url, params=params)
        response = responses[0]

        hourly = response.Hourly()

        return {
            # Convert to numpy arrays for easier processing in scoring
            # This also allows us to use numpy's mean function for averaging
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
            "wind_speed_10m": hourly.Variables(1).ValuesAsNumpy(),
            "relative_humidity_2m": hourly.Variables(2).ValuesAsNumpy(),
            "cloud_cover": hourly.Variables(3).ValuesAsNumpy(),
        }