# 🧠 RAG API — Retrieval-Augmented Generation System

This project implements a **Dockerized RAG (Retrieval-Augmented Generation) API** designed to run efficiently on **CPU-only machines** and handle **100,000+ documents** for question answering. The system uses a modular microservice structure with the following components:

- **API Service (`api/`)** — Hosts endpoints to upload documents and generate answers.
- **Embedding Service (`embedding/`)** — Converts text into vector embeddings using a sentence-transformer model.
- **LLM Generation Service (`ollama/`)** — Uses a local language model (e.g., Qwen2.5-0.5B) via Ollama.
- **Vector Store (`vector_store/`)** — Stores embeddings using ChromaDB.

---

## 🚀 Features

- Upload and index large-scale documents (100k+ with ~5k characters each)
- Query documents with contextual responses from a local LLM
- Optimized for CPU-only environments (<16GB RAM)
- Follows MLOps and modular coding best practices
- Scored with RAGAS metrics for precision and relevance

---

## 🧩 API Endpoints

### 1. `GET /` — API Status Check
```json
{
  "message": "RAG API is running successfully"
}
```

### 2. `POST /upload`
Uploads documents and stores vector embeddings.
#### Request:
```json
{
  "texts": [
    "Document 1 text...",
    "Document 2 text..."
  ]
}
```
#### Response:
```json
{
  "message": "Vector index successfully created",
  "nodes_count": 123
}
```

### 3. `POST /generate`
Generates an answer based on document context.
#### Request:
```json
{
  "new_message": {
    "role": "user",
    "content": "What is the capital of France?"
  }
}
```
#### Response:
```json
{
  "generated_text": "The capital of France is Paris.",
  "contexts": [
    "Paris is the capital of France. It is known for the Eiffel Tower."
  ]
}
```

---

## 🐳 Docker Setup

### Build & Run
```bash
docker-compose up --build
```

### Container Roles
- `api` — FastAPI service running `api_rag.py`
- `embedding` — Embedding service using `embed_server.py`
- `ollama` — Runs local LLM using `start.sh` script

---

## 🧪 Testing

Run the provided test script to verify API:
```bash
python test_api.py
```
This checks all endpoints: status, upload, and generate.

---

## 📁 Project Structure
```
RAG-API/
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
├── test_api.py
└── README.md
```

---

## ✅ Requirements

- Docker v28.0.1
- Docker Compose v2.33.1
- CPU-only machine (≤16GB RAM)

---

## 📦 Submission
Submit `group_X.zip` including:
- All code and configuration files
- `README.md`, `requirements.txt`, and scripts
- `docker-compose.yaml`

---

