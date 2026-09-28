from typing import TypedDict

from app.schemas.response import CandidateMatch


class MatchGraphState(TypedDict):
    job_description: str
    jd_embedding: list[float] | None
    retrieved: list[dict]
    candidates: list[CandidateMatch]
