# Emerging Topics RAG — Retrieval-Augmented Generation System

A Dockerized Retrieval-Augmented Generation (RAG) system optimized for CPU-only environments and capable of indexing and querying large-scale document collections (100k+ documents). This system integrates a modular API, local LLM serving via Ollama, and optional evaluation via RAGAS metrics. Ideal for research or educational deployment, especially in resource-constrained setups.

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
* [Methodology & Findings](#methodology--findings)
* [Project Structure](#project-structure)
* [Use Cases](#use-cases)
* [Limitations & Challenges](#limitations--challenges)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* Upload and index large-scale documents (>100k, \~5k characters each)
* Perform semantic search with contextual answer generation
* CPU-only compatible (≤16GB RAM, no GPU needed)
* Modular microservices: FastAPI, embedding service, LLM wrapper, ChromaDB
* Local LLM inference via Ollama (e.g., Mistral, LLaMA 2)
* RAGAS-ready pipeline for evaluating answer quality and context precision
* Designed for extensibility, benchmarking, and privacy-preserving applications

---

## Prerequisites

* Docker v20.10+
* Docker Compose v1.27+
* CPU-only machine (≥8GB RAM recommended)
* (Optional) `OPENAI_API_KEY` set for metric computation:

```bash
export OPENAI_API_KEY=your_key
```

---

## Getting Started

### Clone the repository with submodules:

```bash
git clone https://github.com/ckranon/emerging-topics-rag.git
cd emerging-topics-rag/rag-api
```


## RAG API Submodule

Located in `rag-api/`, the core RAG pipeline includes:

* `api/` — FastAPI endpoints for document upload and generation
* `embedding/` — Embedding server using `SentenceTransformers`
* `ollama/` — Local LLM runner using [Ollama](https://ollama.com/)
* `vector_store/` — Persistent ChromaDB vector index
* `test_api.py` — Basic integration test script; returns average respones time.
* `compute_metrics.py` — Computes RAGAS Metrics based on generated results from `test_api.py`

## API Endpoints

### `GET /`

Health check:

```bash
curl http://localhost:8000/
```

**Response:**

```json
{"message":"RAG API is running successfully"}
```

---

### `POST /upload`

Uploads documents and indexes them into the vector store.

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"texts":["Document 1 text...", "Document 2 text..."]}'
```

**Response:**

```json
{"message":"Vector index successfully created","nodes_count":123}
```

---

### `POST /generate`

Generates an answer based on user query and retrieved document context.

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

To build and run all services:

```bash
docker-compose up --build
```

**Services launched:**

* `api` — FastAPI service for user interaction
* `embedding` — Generates document embeddings
* `ollama` — Runs a local LLM using `start.sh` <- Can change model.

---

## Testing

### Run API tests:

```bash
python test_api.py
```

### Run RAGAS-based metric evaluation:

```bash
export OPENAI_API_KEY=your_key
python compute_metrics.py
```

> ⚠️ Due to runtime and API constraints, metric computation may timeout.

---

## Methodology & Findings

### Chunking Strategy Evaluation

We compared:

* **Semantic Chunking** — Splitting based on semantic boundaries (embedding similarity)
* **Sentence Window Chunking** — Fixed-size overlapping windows

**Result:**
Inconclusive. `compute_metrics.py` timeout.

---

### Model Comparison

We explored different LLMs:

* **DeepSeek-R1:1.5b** (reasoning-focused, open-weight)
* **Qwen2.5:0.5b** (BASELINE)

**Result:**
Inconclusive. `compute_metrics.py` timeout.

---

### Inference Backends

We tested:

* **[Ollama](https://ollama.com/)** — Seamless local inference with minimal setup
* **[Hugging Face TGI](https://github.com/huggingface/text-generation-inference)** — Scalable backend for multi-GPU serving

**Result:**
Ollama replaced TGI due to TGI not being able to pull baseline models.

---

---

### Vector Stores

Insteaad of using HuggingFace TGI, we implemented a persistent storage using Chroma.db.

---

### Evaluation Issues

Although the pipeline stores generation outputs for downstream evaluation, **RAGAS metric computation consistently timed out** during execution due to:

* API response delays from OpenAI

**As a result**, we deliver a **baseline model** with only qualitative improvement insights and no definitive RAGAS scores.

---

## Project Structure

```
emerging-topics-rag/
├── .gitignore
├── README.md               # This file
├── compute_metrics.py      # Metric computation using RAGAS (OpenAI required)
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
    │   └── chroma.db       # Persistent ChromaDB index
    ├── docker-compose.yaml
    └── test_api.py
```

---

## Use Cases

* **Research Prototypes** — Test chunking and RAG strategies
* **Private Knowledge Retrieval** — Deploy local document Q\&A systems
* **Teaching Tool** — Understand full-stack RAG pipelines
* **Baseline Model Benchmarks** — Evaluate low-resource model performance

---

## Limitations & Challenges

* **RAGAS Metrics Unavailable** — Due to OpenAI API timeout issues
* **No GPU Support** — CPU-only by design; not optimized for high-scale workloads
* **Manual Chunking Trade-offs** — Semantic methods improve results but increase complexity
* **Ollama Model Limitation** — Must manually ensure models are pulled and accessible

---

## Contributing

We welcome contributions!

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Open a pull request

If you find a bug or have a feature request, feel free to open an [Issue](https://github.com/ckranon/emerging-topics-rag/issues).

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code for academic or commercial purposes.

---

(https://github.com/user-attachments/assets/93e5ff9a-f5cb-457f-8637-e410b1058f17)
---

