# Emerging Topics RAG — Retrieval-Augmented Generation System

A Dockerized RAG (Retrieval-Augmented Generation) system optimized for CPU-only environments, capable of indexing and querying large-scale document collections (100k+ documents). This repository includes the RAG API microservices as a Git submodule and integrates a local LLM for low-resource, privacy-preserving inference.

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
* [Use Cases](#use-cases)
* [Limitations & Notes](#limitations--notes)
* [Contributing](#contributing)
* [License](#license)

## Features

* Upload and index large-scale documents (>100k, \~5k characters each)
* Query documents using a locally hosted LLM for contextual responses
* CPU-only compatibility (≤16GB RAM)
* Modular microservices architecture with FastAPI, ChromaDB, and Ollama
* Embedding and querying optimized for quick setup and evaluation
* RAGAS metric scoring for evaluating retrieval+generation performance
* Easily extendable for academic and production scenarios

## Prerequisites

* Docker v20.10+
* Docker Compose v1.27+
* CPU-only machine with ≥8GB RAM (tested with 16GB)
* [Ollama](https://ollama.com/) for running local LLM models
* `OPENAI_API_KEY` environment variable for RAGAS metric testing (CLI only)

## Getting Started

Clone the repository and its submodules:

```bash
git clone https://github.com/ckranon/emerging-topics-rag.git --recursive
cd emerging-topics-rag/rag-api
```

Or, if already cloned:

```bash
git submodule update --init --recursive
cd rag-api
```

## RAG API Submodule

The `rag-api/` folder contains all microservices and orchestration files:

* **api/** — FastAPI REST endpoints
* **embedding/** — SentenceTransformers-based embedding server
* **ollama/** — Wrapper to run LLMs using Ollama locally
* **vector\_store/** — ChromaDB persistent vector storage

## API Endpoints

### GET /

Health check for the API service.

```bash
curl http://localhost:8000/
```

**Response:**

```json
{"message":"RAG API is running successfully"}
```

---

### POST /upload

Uploads a batch of documents to be embedded and stored in the vector index.

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"texts":["Document 1...","Document 2..."]}'
```

**Response:**

```json
{"message":"Vector index successfully created","nodes_count":123}
```

---

### POST /generate

Generates an answer from the documents using semantic retrieval and a local LLM.

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"new_message":{"role":"user","content":"What is the capital of France?"}}'
```

**Response:**

```json
{
  "generated_text": "The capital of France is Paris.",
  "contexts": ["Paris is the capital of France. It is known for the Eiffel Tower."]
}
```

---

## Docker Setup

Spin up the system with:

```bash
docker-compose up --build
```

**Services:**

* `api` — FastAPI server with endpoints
* `embedding` — Embedding server for vector creation
* `ollama` — Local LLM runner (e.g., LLaMA 2, Mistral)

Ensure Ollama is installed and the desired model (e.g., `mistral`, `llama2`) is available locally via `ollama run`.

## Testing

Run the test script to validate core endpoints:

```bash
python test_api.py
```

Evaluate RAG performance with:

```bash
export OPENAI_API_KEY=your_key
python compute_metrics.py
```

This script uses RAGAS to measure:

* Faithfulness
* Context precision
* Answer relevance

## Project Structure

```
emerging-topics-rag/
├── .gitignore
├── README.md               # This file
├── compute_metrics.py      # RAGAS-based metric computation script
└── rag-api/
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
    │   └── chroma.db       # Chroma vector index storage
    ├── docker-compose.yaml
    └── test_api.py
```

## Use Cases

* **Academic Research** — Evaluate retrieval systems on large corpora
* **Enterprise Search** — Private document retrieval without external APIs
* **Education** — Build understanding of full-stack RAG systems
* **Prototyping** — Quickly test ideas with a plug-and-play RAG setup

## Limitations & Notes

* This system is designed for low-resource (CPU-only) environments and may not be ideal for high-throughput applications.
* Currently supports basic document chunking; advanced chunking/token control is left to the user.
* Ollama must be installed separately and run in advance with a local model pulled.
* For large document sets, consider running embedding and querying in batches.

## Contributing

We welcome contributions from the community! Please:

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Open a pull request

For bugs or suggestions, feel free to open an [issue](https://github.com/ckranon/emerging-topics-rag/issues).

## License

MIT License. See the [LICENSE](LICENSE) file for details.
