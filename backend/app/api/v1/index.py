from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.deps import get_index_service
from app.application.index_service import IndexService
from app.schemas.index import IndexResponse

router = APIRouter()


@router.post("/index", response_model=IndexResponse)
async def index_documents(
    files: list[UploadFile] = File(...),
    service: IndexService = Depends(get_index_service),
) -> IndexResponse:
    try:
        return await service.index_files(files)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
