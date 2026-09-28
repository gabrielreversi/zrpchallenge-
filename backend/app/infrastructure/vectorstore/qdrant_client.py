import logging
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.domain.models import RetrievedCandidate
from app.infrastructure.config import Settings

logger = logging.getLogger(__name__)


class QdrantCandidateStore:
    def __init__(self, settings: Settings) -> None:
        self._collection = settings.qdrant_collection
        self._client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key or None,
        )

    def ensure_collection(self, vector_size: int) -> None:
        if self._client.collection_exists(self._collection):
            return
        self._client.create_collection(
            collection_name=self._collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def upsert_documents(
        self,
        points: list[dict],
    ) -> list[str]:
        """Upsert points. Each dict: id, vector, payload."""
        if not points:
            return []
        vector_size = len(points[0]["vector"])
        self.ensure_collection(vector_size)

        structs = [
            PointStruct(
                id=self._to_point_id(point["id"]),
                vector=point["vector"],
                payload=point["payload"],
            )
            for point in points
        ]
        self._client.upsert(collection_name=self._collection, points=structs)
        return [str(point["id"]) for point in points]

    def search(self, vector: list[float], limit: int = 3) -> list[RetrievedCandidate]:
        try:
            points = self._client.query_points(
                collection_name=self._collection,
                query=vector,
                limit=limit,
                with_payload=True,
            ).points
        except UnexpectedResponse as exc:
            logger.warning("Qdrant search failed (collection missing or error): %s", exc)
            return []
        except Exception as exc:  # noqa: BLE001
            logger.warning("Qdrant search unavailable: %s", exc)
            return []

        results: list[RetrievedCandidate] = []
        for point in points:
            payload = point.payload or {}
            name = str(payload.get("name", "")).strip()
            cv_text = str(payload.get("cv_text", "")).strip()
            if not name:
                continue
            results.append(
                RetrievedCandidate(
                    candidate_id=str(payload.get("candidate_id", point.id)),
                    name=name,
                    cv_text=cv_text,
                    score=float(point.score or 0.0),
                )
            )
        return results

    @staticmethod
    def _to_point_id(candidate_id: str) -> str:
        """Qdrant accepts UUID or unsigned int; map string ids to UUIDv5."""
        try:
            uuid.UUID(candidate_id)
            return candidate_id
        except ValueError:
            return str(uuid.uuid5(uuid.NAMESPACE_URL, f"candidate:{candidate_id}"))
