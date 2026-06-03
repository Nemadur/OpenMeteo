import asyncio

from app.clients.openMeteoClient import OpenMeteoClient
from app.services.scoringService import ScoringService

class WeatherService:

    def __init__(self):
        self.client = OpenMeteoClient()
        self.semaphore = asyncio.Semaphore(2)

    # Limit concurrent processing to avoid hitting API rate limits
    async def safe_process(self, city, start_date, end_date):
        async with self.semaphore:
            return await self._process_city(city, start_date, end_date)

    async def rank_cities(
        self,
        cities: list[str],
        start_date: str,
        end_date: str
    ):
        # Process cities in parallel as they are independent of each other
        results = await asyncio.gather(
            *[
                self.safe_process(city, start_date, end_date)
                for city in cities
            ]
        )

        # Sort cities by score in descending order
        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    async def _process_city(
        self,
        city: str,
        start_date: str,
        end_date: str
    ):
        # Take coordinates as app doesn't accept city names directly
        coordinates = (
            self.client.geocode_city(city)
        )

        # Fetch weather data for the city and calculate score based on it
        weather = (
            self.client.fetch_weather(
                coordinates["latitude"],
                coordinates["longitude"],
                start_date,
                end_date,
            )
        )

        score = ScoringService.calculate(weather)

        return {
            "city": city,
            "score": score,
        }