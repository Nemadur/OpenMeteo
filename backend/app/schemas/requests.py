from pydantic import BaseModel
from typing import  Optional

class RankingRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None