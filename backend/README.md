# Curadoria de Talentos — Backend

API FastAPI (layer architecture) com LangGraph, Qdrant (busca semântica Top 3) e Azure OpenAI.

**Nesta fase não há indexação/seed.** A busca retorna lista vazia se a collection não tiver pontos.

## Setup

```bash
cp .env.example .env
# preencha as chaves Azure OpenAI

poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Com Docker (backend + Qdrant):

```bash
# na raiz do monorepo
cp backend/.env.example backend/.env
docker compose up --build
```

## Endpoints

- `GET /health` — liveness
- `POST /api/v1/match` — body `{ "job_description": "..." }`
- `POST /api/v1/index` — multipart `files` (`.txt`, múltiplos)

## Spec

- [document/SDD-backend.md](../document/SDD-backend.md)
- [document/SDD-indexacao.md](../document/SDD-indexacao.md)
