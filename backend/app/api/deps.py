from functools import lru_cache

from app.application.index_service import IndexService
from app.application.match_service import MatchService
from app.infrastructure.config import Settings, get_settings
from app.infrastructure.llm.chat import ChatService
from app.infrastructure.llm.embeddings import EmbeddingService
from app.infrastructure.vectorstore.qdrant_client import QdrantCandidateStore


@lru_cache
def _settings() -> Settings:
    return get_settings()


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(_settings())


@lru_cache
def get_qdrant_store() -> QdrantCandidateStore:
    return QdrantCandidateStore(_settings())


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(_settings())


@lru_cache
def get_match_service() -> MatchService:
    return MatchService(
        embeddings=get_embedding_service(),
        store=get_qdrant_store(),
        chat=get_chat_service(),
    )


@lru_cache
def get_index_service() -> IndexService:
    return IndexService(
        embeddings=get_embedding_service(),
        store=get_qdrant_store(),
    )


def get_app_settings() -> Settings:
    return _settings()
