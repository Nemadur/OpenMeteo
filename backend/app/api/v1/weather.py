from fastapi import APIRouter

from app.schemas.requests import RankingRequest
from app.services.weatherService import WeatherService
from app.utils.utils import get_default_dates

router = APIRouter()

service = WeatherService()

@router.post("/cities-scores")
async def rank_cities(
    request: RankingRequest
):
    start_date = request.start_date
    end_date = request.end_date
    cities = ["Warsaw", "Gdansk", "Berlin", "Krakow", "Nurnberg", "Munich"]

    if not start_date or not end_date:
        start_date, end_date = (
            get_default_dates()
        )

    results = await service.rank_cities(
        cities,
        start_date,
        end_date,
    )

    rankings = []

    for index, city in enumerate(results, start=1):
        rankings.append(
            {
                "rank": index,
                **city
            }
        )

    return {
        "rankings": rankings
    }