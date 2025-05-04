# Emerging Topics RAG — Retrieval-Augmented Generation System

A Dockerized RAG (Retrieval-Augmented Generation) system optimized for CPU-only environments, capable of indexing and querying large-scale document collections (100k+ documents). This repository includes the RAG API microservices as a git submodule.

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
* [RAG API Submodule](#rag-api-submodule)
* [API Endpoints](#api-endpoints)

  * [GET /](#get-)
  * [POST /upload](#post-upload)
  * [POST /generate](#post-generate)
* [Docker Setup](#docker-setup)
* [Testing](#testing)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)

## Features

* Upload and index large-scale documents (>100k, \~5k characters each)
* Query documents with contextual responses from a local LLM
* CPU-only operation (<16GB RAM)
* Modular microservices following MLOps best practices
* Scored with RAGAS metrics for precision and relevance

## Prerequisites

* Docker v20.10+
* Docker Compose v1.27+
* CPU-only machine (≤16GB RAM)
* [Ollama](https://ollama.com/) installed for local LLM serving
* **Environment variable**: set `OPENAI_API_KEY` for CLI usage (e.g., `export OPENAI_API_KEY=your_key`)

## Getting Started

Clone the repository with submodules:

```bash
git clone https://github.com/ckranon/emerging-topics-rag.git --recursive
cd emerging-topics-rag/rag-api
```

Or, if you have already cloned:

```bash
git submodule update --init --recursive
cd rag-api
```

## RAG API Submodule

The `rag-api/` directory contains the microservice components:

* **api/** — FastAPI endpoints (`api_rag.py`)
* **embedding/** — Embedding server (`embed_server.py`)
* **ollama/** — Local LLM runner (`start.sh`)
* **vector\_store/** — ChromaDB vector index

## API Endpoints

### GET /

Status check:

```bash
curl http://localhost:8000/
# {"message":"RAG API is running successfully"}
```

### POST /upload

Uploads and indexes documents.

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"texts":["Document 1 text...","Document 2 text..."]}'
```

**Response:**

```json
{"message":"Vector index successfully created","nodes_count":123}
```

### POST /generate

Generates answers based on document context.

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"new_message":{"role":"user","content":"What is the capital of France?"}}'
```

**Response:**

```json
{
  "generated_text":"The capital of France is Paris.",
  "contexts":["Paris is the capital of France. It is known for the Eiffel Tower."]
}
```

## Docker Setup

Build and run all services:

```bash
docker-compose up --build
```

* **api** — runs FastAPI (`api_rag.py`)
* **embedding** — runs embedding server (`embed_server.py`)
* **ollama** — runs LLM via `start.sh`

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

Compute RAG metrics via CLI (requires `OPENAI_API_KEY`):

```bash
export OPENAI_API_KEY=your_key
python compute_metrics.py
```

## Project Structure

```
emerging-topics-rag/
├── .gitignore
├── README.md         # this file
├── compute_metrics.py # script to compute RAG metrics via CLI (requires OPENAI_API_KEY)
└── rag-api/          # submodule with RAG microservices
    ├── api/
    │   ├── api_rag.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── embedding/
    │   ├── embed_server.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── ollama/
    │   ├── start.sh
    │   └── Dockerfile
    ├── vector_store/
    │   └── chroma.db
    ├── docker-compose.yaml
    └── test_api.py
```

## Contributing

Contributions are welcome! Please fork the repo, make your changes, and submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
