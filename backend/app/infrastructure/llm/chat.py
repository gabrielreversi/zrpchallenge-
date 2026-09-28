from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field

from app.domain.prompts import SYSTEM_PROMPT, build_justify_user_prompt
from app.infrastructure.config import Settings
from app.schemas.response import CandidateMatch


class _JustificationItem(BaseModel):
    rank: int = Field(..., ge=1)
    name: str
    justification: str


class _JustificationBatch(BaseModel):
    candidates: list[_JustificationItem]


class ChatService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._llm: AzureChatOpenAI | None = None

    def _client(self) -> AzureChatOpenAI:
        if self._llm is None:
            if not self._settings.azure_openai_api_key or not self._settings.azure_openai_endpoint:
                raise RuntimeError(
                    "Azure OpenAI não configurado. Defina AZURE_OPENAI_API_KEY e AZURE_OPENAI_ENDPOINT."
                )
            self._llm = AzureChatOpenAI(
                azure_endpoint=self._settings.azure_openai_endpoint,
                api_key=self._settings.azure_openai_api_key,
                api_version=self._settings.azure_openai_api_version,
                azure_deployment=self._settings.azure_openai_chat_deployment,
                temperature=0.2,
            )
        return self._llm

    def justify_matches(
        self,
        job_description: str,
        retrieved: list[dict],
    ) -> list[CandidateMatch]:
        if not retrieved:
            return []

        lines: list[str] = []
        for index, item in enumerate(retrieved, start=1):
            lines.append(
                f"#{index} | name={item['name']}\nCV:\n{item['cv_text']}\n"
            )
        candidates_block = "\n".join(lines)

        structured = self._client().with_structured_output(_JustificationBatch)
        result = structured.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=build_justify_user_prompt(
                        job_description,
                        candidates_block,
                    )
                ),
            ]
        )

        if isinstance(result, dict):
            batch = _JustificationBatch.model_validate(result)
        else:
            batch = result

        return [
            CandidateMatch(
                rank=item.rank,
                name=item.name,
                justification=item.justification,
            )
            for item in batch.candidates
        ]
