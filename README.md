# Curadoria de Talentos — Match-Making Executivo

Protótipo end-to-end de um **agente de curadoria de talentos** para consultoria de alto nível: a partir de um **Job Description (JD)**, o sistema busca semanticamente currículos em uma base vetorial e devolve um **Top 3** com justificativa **analítica e consultiva** (apoio à decisão dos sócios, não substituição).

Desafio técnico: **Cientista de Dados Sênior / AI Engineer**.

---

## Problema de negócio

Consultorias de executive search lidam com:

- JDs complexos e currículos **não estruturados**
- Decisão subjetiva de fit (hard + soft skills) em nível C-Level
- Dados sensíveis de executivos (privacidade)
- Necessidade de output com **tom estratégico**, útil para sócios em modelo de partnership

O objetivo é acelerar a curadoria com RAG + LLM, mantendo o humano no loop.

---

## Solução

| Capacidade | Descrição |
|------------|-----------|
| **Indexação** | Upload de um ou mais `.txt` (mini-CVs); cada arquivo vira **1 vetor** no Qdrant (sem chunking nesta versão) |
| **Match** | Cola-se o JD → embedding → busca semântica Top 3 → LLM gera justificativas consultivas |
| **UI** | React minimalista: login fake, abas Curadoria e Indexação |

---

## Como rodar

### Pré-requisitos

- Docker + Docker Compose
- Node.js 20+ (frontend)
- Conta Azure OpenAI com deployments de **embedding** e **chat**
- (Opcional) Poetry 2.x se for rodar a API fora do Docker

### 1. Variáveis de ambiente

```bash
cp backend/.env.example backend/.env
```

Preencha no mínimo:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` → `text-embedding-3-small` (nome do deployment no Azure)
- `AZURE_OPENAI_CHAT_DEPLOYMENT` → `gpt-4.1-mini` (nome do deployment no Azure)

No `docker compose`, o backend recebe `QDRANT_URL=http://qdrant:6333` automaticamente.

**Não versionar** o arquivo `.env` com secrets.

### 2. Backend + Qdrant (Docker)

Na raiz do repositório:

```bash
docker compose up --build
```

| Recurso | URL |
|---------|-----|
| API | http://localhost:8000 |
| Health | http://localhost:8000/health |
| OpenAPI | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

### 3. Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Abra o endereço do Vite (em geral http://localhost:5173).  
`VITE_API_BASE_URL` deve apontar para `http://localhost:8000`.

### 4. Fluxo de uso

1. Login fake (qualquer usuário/senha)
2. Aba **Indexação** → selecione `document/candA.txt` … `candD.txt` → **Indexar** (mensagem verde = sucesso)
3. Aba **Curadoria** → cole um JD → **Analisar candidatos** → Top 3

### Alternativa: API local + só Qdrant no Docker

```bash
docker compose up -d qdrant
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Arquitetura

```text
┌─────────────┐     HTTP/JSON      ┌─────────────┐      ┌─────────┐
│  frontend   │ ─────────────────► │   backend   │ ───► │ qdrant  │
│ React/Vite  │                    │  FastAPI    │      │ Docker  │
└─────────────┘                    └──────┬──────┘      └─────────┘
                                          │
                                          ▼
                                   Azure OpenAI
                     (text-embedding-3-small + gpt-4.1-mini)
```

### Containers (`docker-compose.yml`)

| Serviço | Função |
|---------|--------|
| `qdrant` | Banco vetorial local (imagem `qdrant/qdrant`) |
| `backend` | API FastAPI + LangGraph |

O frontend roda em desenvolvimento via npm (ainda fora do Compose).

---

## Estrutura de pastas

```text
zrpchallenge/
├── document/                 # Briefing, SDDs, mini-CVs (.txt)
├── frontend/                 # React + Vite + TypeScript
├── backend/                  # FastAPI + Poetry + layers
│   └── app/
│       ├── api/              # Rotas HTTP
│       ├── application/      # Casos de uso + LangGraph
│       ├── domain/           # Regras / prompts / parse
│       ├── infrastructure/   # Azure, Qdrant, settings
│       └── schemas/          # DTOs Pydantic
├── docker-compose.yml
└── README.md
```

---

## Arquitetura de software (backend)

### Layer architecture

| Camada | Responsabilidade |
|--------|------------------|
| `api` | FastAPI, validação HTTP, status codes |
| `application` | `MatchService`, `IndexService`, grafo LangGraph |
| `domain` | Prompts consultivos, parse de nome do CV |
| `infrastructure` | Azure OpenAI, Qdrant, `pydantic-settings` |

### LangGraph (match)

```text
embed_jd → retrieve_top3 → justify_matches
```

1. Gera embedding do JD  
2. Busca semântica Top 3 no Qdrant  
3. LLM produz justificativas consultivas (sem inventar skills ausentes no CV)

---

## Stack

| Camada | Tecnologia |
|--------|------------|
| Frontend | React, Vite, TypeScript, React Router |
| Backend | Python 3.11+, FastAPI, Uvicorn, Poetry |
| Orquestração | LangGraph, LangChain OpenAI |
| Validação | Pydantic v2 / pydantic-settings |
| Vector DB | Qdrant (container Docker local) |
| LLM / Embed | Azure OpenAI |
| Observabilidade | LangSmith (opcional via env) |

---

## Tipo de busca (RAG)

- **Busca semântica** por similaridade de cosseno no Qdrant
- O JD é convertido em embedding; recupera-se o **Top 3** currículos
- Em seguida o LLM redige a justificativa com tom consultivo
- Indexação atual: **documento inteiro** (sem chunking), adequada aos mini-CVs do desafio

---

## Modelos utilizados

| Papel | Modelo / deployment |
|-------|---------------------|
| Embedding | `text-embedding-3-small` |
| Completion (chat) | `gpt-4.1-mini` |

Os nomes em `AZURE_OPENAI_*_DEPLOYMENT` devem coincidir com os **deployments** do recurso Azure OpenAI.

---

## Endpoints principais

| Método | Path | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Liveness |
| `POST` | `/api/v1/index` | Multipart `files` — indexa `.txt` |
| `POST` | `/api/v1/match` | `{ "job_description": "..." }` — Top 3 |

---

## Atendimento ao desafio

- Agente end-to-end com LLM + orquestração (LangGraph)
- Pipeline RAG com banco vetorial (Qdrant)
- Top 3 + justificativa consultiva
- UI para o sócio (colar JD / indexar CVs)
- Dados fictícios em `document/cand*.txt`
- Privacidade: dados e keys só em ambiente local / `.env`

Expectativa de teste do briefing:

- Vaga CTO / IA hands-on → tendência a **Carolina Mendes**
- Vaga CFO / captação / M&A → tendência a **Ana Silva**

---

## Limitações e próximos passos

- Sem chunking / re-ranker avançado
- Login fake (sem autenticação real)
- Frontend ainda fora do Compose
- LangSmith opcional
- Visão de produção (ex.: GCP Cloud Run + Qdrant gerenciado) pode ser detalhada na apresentação

---

## Documentação adicional

| Arquivo | Conteúdo |
|---------|----------|
| [`document/Desafio_Cientista_de_Dados_Senior-v2.pdf`](document/Desafio_Cientista_de_Dados_Senior-v2.pdf) | Briefing do desafio |
| [`document/SDD.md`](document/SDD.md) | Visão geral |
| [`document/SDD-backend.md`](document/SDD-backend.md) | Backend |
| [`document/SDD-indexacao.md`](document/SDD-indexacao.md) | Upload / indexação |
| [`document/SDD-readme.md`](document/SDD-readme.md) | Spec deste README |
| [`backend/README.md`](backend/README.md) | Notas rápidas da API |
| [`frontend/README.md`](frontend/README.md) | Notas rápidas do front |
