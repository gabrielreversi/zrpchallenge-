from app.application.graph.state import MatchGraphState
from app.infrastructure.llm.chat import ChatService
from app.infrastructure.llm.embeddings import EmbeddingService
from app.infrastructure.vectorstore.qdrant_client import QdrantCandidateStore
from app.schemas.response import CandidateMatch


def make_nodes(
    embeddings: EmbeddingService,
    store: QdrantCandidateStore,
    chat: ChatService,
):
    def embed_jd(state: MatchGraphState) -> dict:
        vector = embeddings.embed_text(state["job_description"])
        return {"jd_embedding": vector}

    def retrieve_top3(state: MatchGraphState) -> dict:
        embedding = state.get("jd_embedding")
        if not embedding:
            return {"retrieved": []}
        hits = store.search(embedding, limit=3)
        return {
            "retrieved": [
                {
                    "candidate_id": hit.candidate_id,
                    "name": hit.name,
                    "cv_text": hit.cv_text,
                    "score": hit.score,
                }
                for hit in hits
            ]
        }

    def justify_matches(state: MatchGraphState) -> dict:
        retrieved = state.get("retrieved") or []
        if not retrieved:
            return {"candidates": []}

        generated = chat.justify_matches(
            job_description=state["job_description"],
            retrieved=retrieved,
        )
        by_name = {item.name.strip().lower(): item for item in generated}

        candidates: list[CandidateMatch] = []
        for index, item in enumerate(retrieved, start=1):
            key = item["name"].strip().lower()
            matched = by_name.get(key)
            justification = (
                matched.justification
                if matched
                else (
                    "Perfil recuperado por similaridade semântica; "
                    "justificativa consultiva indisponível."
                )
            )
            candidates.append(
                CandidateMatch(
                    rank=index,
                    name=item["name"],
                    justification=justification,
                )
            )
        return {"candidates": candidates}

    return embed_jd, retrieve_top3, justify_matches
