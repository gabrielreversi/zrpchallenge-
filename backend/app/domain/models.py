from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedCandidate:
    candidate_id: str
    name: str
    cv_text: str
    score: float


@dataclass(frozen=True)
class RankedCandidate:
    rank: int
    name: str
    justification: str
