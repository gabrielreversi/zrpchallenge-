from fastapi import UploadFile

from app.domain.candidate_parse import candidate_id_from_filename, extract_candidate_name
from app.infrastructure.llm.embeddings import EmbeddingService
from app.infrastructure.vectorstore.qdrant_client import QdrantCandidateStore
from app.schemas.index import IndexedItem, IndexResponse


class IndexService:
    def __init__(
        self,
        embeddings: EmbeddingService,
        store: QdrantCandidateStore,
    ) -> None:
        self._embeddings = embeddings
        self._store = store

    async def index_files(self, files: list[UploadFile]) -> IndexResponse:
        if not files:
            raise ValueError("Nenhum arquivo enviado.")

        prepared: list[dict] = []
        meta: list[tuple[str, str, str]] = []

        for upload in files:
            filename = upload.filename or "arquivo.txt"
            if not filename.lower().endswith(".txt"):
                raise ValueError(f"Arquivo inválido (apenas .txt): {filename}")

            raw = await upload.read()
            try:
                text = raw.decode("utf-8").strip()
            except UnicodeDecodeError as exc:
                raise ValueError(f"Arquivo não é UTF-8 válido: {filename}") from exc

            if not text:
                raise ValueError(f"Arquivo vazio: {filename}")

            candidate_id = candidate_id_from_filename(filename)
            name = extract_candidate_name(text, filename)
            vector = self._embeddings.embed_text(text)

            prepared.append(
                {
                    "id": candidate_id,
                    "vector": vector,
                    "payload": {
                        "candidate_id": candidate_id,
                        "name": name,
                        "cv_text": text,
                        "source_filename": filename,
                    },
                }
            )
            meta.append((filename, name, candidate_id))

        self._store.upsert_documents(prepared)

        items = [
            IndexedItem(filename=filename, name=name, point_id=point_id)
            for filename, name, point_id in meta
        ]
        return IndexResponse(indexed_count=len(items), items=items)
