from pydantic import BaseModel, Field


class CandidateMatch(BaseModel):
    rank: int = Field(..., ge=1)
    name: str
    justification: str


class MatchResponse(BaseModel):
    candidates: list[CandidateMatch]
