# mini-RAG

Minimal FastAPI service for document ingestion and chunking in a Retrieval-Augmented Generation (RAG) workflow.

The project is a production-style follow-up to the course [mini-RAG | From notebooks to PRODUCTION](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj), with a simple API that:

- accepts uploaded files (`.txt`, `.pdf`),
- stores them under project-scoped folders,
- processes them into text chunks using LangChain splitters.

## Project Overview

### Purpose

This service provides the ingestion and preprocessing layer of a RAG pipeline. It is intended for developers who want a lightweight backend to:

- upload source documents,
- split content into retrieval-friendly chunks,
- return chunked content for downstream embedding/storage/retrieval systems.

### Primary Use Cases

- Rapid prototyping of RAG ingestion APIs.
- Local experimentation with chunk size and overlap strategies.
- Building a foundation before adding vector DB indexing and LLM query paths.

## Architecture At a Glance

Current flow:

1. FastAPI app starts and initializes a MongoDB client in the app lifespan.
2. Client uploads a file to `/api/v1/data/upload/{project_id}`.
3. File is validated (MIME type, size), sanitized, and saved to `src/assets/files/{project_id}/`.
4. Client calls `/api/v1/data/process/{project_id}` with `file_id`, `chunk_size`, and `overlap_size`.
5. Service loads file content (`TextLoader` for `.txt`, `PyMuPDFLoader` for `.pdf`) and splits it with `RecursiveCharacterTextSplitter`.
6. API returns chunked documents.

Notes:

- MongoDB connectivity is configured and initialized, but chunk/project persistence is not currently implemented.
- The `do_reset` request field exists in schema but is not used in processing logic yet.

## Tech Stack

- Python 3.11
- FastAPI + Uvicorn
- Pydantic / pydantic-settings
- LangChain + langchain-community + langchain-text-splitters
- PyMuPDF (PDF loading)
- Motor + PyMongo (MongoDB connectivity)
- aiofiles (async file writes)
- uv (environment + dependency manager)
- Docker Compose (MongoDB service)

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker (optional, for MongoDB via Compose)

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment variables

Copy the sample file:

```bash
cp src/.env.example src/.env
```

On PowerShell:

```powershell
Copy-Item src/.env.example src/.env
```

Then edit `src/.env`.

### 3. Start MongoDB (optional but recommended)

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 4. Run the API

From the repository root:

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Alternative:

```bash
cd src
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Verify

- Open `http://127.0.0.1:8000/docs` for Swagger UI.
- Health-style welcome endpoint: `GET http://127.0.0.1:8000/api/v1/`.

## Installation Details

### Recommended: uv

```bash
uv sync
```

### Alternative: pip

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Environment is loaded from `src/.env` via `pydantic-settings`.

### Required variables

| Variable                  | Description                          | Example                             |
| ------------------------- | ------------------------------------ | ----------------------------------- |
| `APP_NAME`                | Display name in welcome response     | `Mini-RAG`                          |
| `APP_VERSION`             | App version in welcome response      | `0.1.0`                             |
| `APP_ENV`                 | Environment name                     | `development`                       |
| `GROQ_API_KEY`            | Reserved for future LLM integrations | `...`                               |
| `FILE_ALLOWED_TYPES`      | Allowed MIME types for upload        | `["text/plain", "application/pdf"]` |
| `FILE_MAX_SIZE_MB`        | Max upload size (MB)                 | `10`                                |
| `FILE_DEFAULT_CHUNK_SIZE` | Upload stream chunk size (bytes)     | `512000`                            |
| `MONGODB_URL`             | MongoDB connection string            | `mongodb://localhost:27007`         |
| `MONGODB_DATABASE`        | DB name                              | `mini_rag`                          |

## API Usage

Base URL: `http://127.0.0.1:8000`

### 1. Welcome

`GET /api/v1/`

Response includes app metadata and a welcome message.

### 2. Upload a file

`POST /api/v1/data/upload/{project_id}`

- Content type: `multipart/form-data`
- Form field name: `file`
- Valid MIME types: `text/plain`, `application/pdf`

Example:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/data/upload/5" \
	-F "file=@src/assets/mini-rag.txt"
```

Success response:

```json
{
	"message": "File uploaded successfully",
	"file_id": "<randomPrefix>_<cleanedFilename>"
}
```

### 3. Process a file into chunks

`POST /api/v1/data/process/{project_id}`

Request body:

```json
{
	"file_id": "CqdsuhCnVOot_mini-rag.txt",
	"chunk_size": 400,
	"overlap_size": 30,
	"do_reset": 0
}
```

Returns a JSON array of chunk documents (content + metadata) generated by LangChain.

## Postman Assets

The repository includes ready-to-run Postman request definitions in:

- `postman/collections/mini-rag/welcome-request api-v1 (health-check).request.yaml`
- `postman/collections/mini-rag/upload.request.yaml`
- `postman/collections/mini-rag/process.request.yaml`

Collection variable defaults are in:

- `postman/collections/mini-rag/.resources/definition.yaml`

## Project Structure

```text
mini-rag/
├── pyproject.toml                # Project metadata and dependency spec (uv)
├── requirements.txt              # Exported pinned dependencies
├── uv.lock                       # Lockfile for reproducible installs
├── docker/
│   └── docker-compose.yml        # MongoDB container definition
├── postman/
│   ├── collections/mini-rag/     # API request definitions
│   └── globals/                  # Postman globals
└── src/
    ├── main.py                   # FastAPI app + lifespan (Mongo client)
    ├── helpers/config.py         # Pydantic settings loading from src/.env
    ├── routes/
    │   ├── base.py               # /api/v1 welcome endpoint
    │   └── data.py               # upload/process endpoints
    ├── routes/schemes/data.py    # Process request schema
    ├── controllers/
    │   ├── BaseController.py     # shared paths and utilities
    │   ├── DataController.py     # upload validation + unique file naming
    │   ├── ProjectController.py  # project directory management
    │   └── ProcessController.py  # file loading + chunking logic
    ├── models/
    │   ├── enums/                # processing and response enums
    │   └── db_schemes/           # Pydantic DB models (not yet wired)
    └── assets/
        └── files/                # uploaded files grouped by project_id
```

## Development

### Run in development mode

```bash
uv run uvicorn src.main:app --reload
```

### API docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Tests and quality checks

- No automated test suite is currently present.
- No lint/format/type-check commands are currently configured in project metadata.

Recommended next additions:

1. Add `pytest` tests for routes/controllers.
2. Add `ruff` and/or `black` for code quality.
3. Add CI checks for formatting, linting, and tests.

### Build and deployment status

- Docker Compose currently provisions MongoDB only.
- The FastAPI app itself is not containerized in this repository yet.

## Troubleshooting

### `ModuleNotFoundError` when starting app

Use one of these commands from repo root:

- `uv run uvicorn src.main:app --reload`
- or `cd src` then `uv run uvicorn main:app --reload`

### Validation errors on startup (missing settings)

Ensure `src/.env` exists and contains all required variables from `src/.env.example`.

### File upload rejected

Check:

- `file` form field name is correct,
- MIME type is allowed (`text/plain` or `application/pdf`),
- file size does not exceed `FILE_MAX_SIZE_MB`.

### MongoDB connection issues

- Confirm container is running: `docker ps`
- Confirm `MONGODB_URL` matches your environment (default Compose mapping is `mongodb://localhost:27007`).

## License and Attribution

- License: No license file is currently present in this repository.
- Attribution: Inspired by the course [mini-RAG | From notebooks to PRODUCTION](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj).