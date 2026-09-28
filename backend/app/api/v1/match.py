from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_match_service
from app.application.match_service import MatchService
from app.schemas.request import MatchRequest
from app.schemas.response import MatchResponse

router = APIRouter()


@router.post("/match", response_model=MatchResponse)
def create_match(
    body: MatchRequest,
    service: MatchService = Depends(get_match_service),
) -> MatchResponse:
    try:
        return service.match(body)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
