from app.application.graph.workflow import build_match_graph
from app.infrastructure.llm.chat import ChatService
from app.infrastructure.llm.embeddings import EmbeddingService
from app.infrastructure.vectorstore.qdrant_client import QdrantCandidateStore
from app.schemas.request import MatchRequest
from app.schemas.response import MatchResponse


class MatchService:
    def __init__(
        self,
        embeddings: EmbeddingService,
        store: QdrantCandidateStore,
        chat: ChatService,
    ) -> None:
        self._graph = build_match_graph(embeddings, store, chat)

    def match(self, request: MatchRequest) -> MatchResponse:
        result = self._graph.invoke(
            {
                "job_description": request.job_description.strip(),
                "jd_embedding": None,
                "retrieved": [],
                "candidates": [],
            }
        )
        return MatchResponse(candidates=result.get("candidates") or [])
