from pydantic import BaseModel, Field


class IndexedItem(BaseModel):
    filename: str
    name: str
    point_id: str


class IndexResponse(BaseModel):
    indexed_count: int = Field(..., ge=0)
    items: list[IndexedItem]
