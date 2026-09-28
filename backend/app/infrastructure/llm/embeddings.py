from langchain_openai import AzureOpenAIEmbeddings

from app.infrastructure.config import Settings


class EmbeddingService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._embeddings: AzureOpenAIEmbeddings | None = None

    def _client(self) -> AzureOpenAIEmbeddings:
        if self._embeddings is None:
            if not self._settings.azure_openai_api_key or not self._settings.azure_openai_endpoint:
                raise RuntimeError(
                    "Azure OpenAI não configurado. Defina AZURE_OPENAI_API_KEY e AZURE_OPENAI_ENDPOINT."
                )
            self._embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=self._settings.azure_openai_endpoint,
                api_key=self._settings.azure_openai_api_key,
                api_version=self._settings.azure_openai_api_version,
                azure_deployment=self._settings.azure_openai_embedding_deployment,
            )
        return self._embeddings

    def embed_text(self, text: str) -> list[float]:
        return self._client().embed_query(text)
