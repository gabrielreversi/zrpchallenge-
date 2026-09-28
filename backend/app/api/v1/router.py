from fastapi import APIRouter

from app.api.v1 import index, match

router = APIRouter(prefix="/api/v1")
router.include_router(match.router)
router.include_router(index.router)
