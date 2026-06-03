from pydantic import BaseModel

class CityRanking(BaseModel):
    rank: int
    city: str
    score: float

class RankingResponse(BaseModel):
    rankings: list[CityRanking]