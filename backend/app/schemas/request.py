from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    job_description: str = Field(..., min_length=1)
