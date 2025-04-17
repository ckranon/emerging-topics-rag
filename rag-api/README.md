# rag_api/README.md

## 📦 RAG API Assignment - CPU Only, Dockerized

This project implements a lightweight, modular Retrieval-Augmented Generation (RAG) API capable of handling up to 100,000 documents (~5,000 characters each) on a CPU-only machine (max 16GB RAM). It uses:

- 🧠 **LlamaIndex** for RAG pipeline
- 🔎 **Chroma** as the vector store
- 🤗 **BAAI/bge-small-en** for embeddings
- 💬 **Ollama + Qwen 0.5B** for local language generation

---

## 🔧 Architecture Overview

- `api/`: Main FastAPI app
- `embedding/`: Embedding service container
- `ollama/`: LLM generation service (via Ollama)

These are orchestrated using `docker-compose`.

---

## 🚀 How to Run

1. **Install Docker & Docker Compose** (per assignment spec)

2. **Start services**:
```bash
docker compose up --build
```

3. **Verify API**:
```bash
curl http://localhost:8000/
```
Should return:
```json
{"message": "RAG API is running successfully"}
```

---

## 📤 POST /upload
**Upload a list of documents**
```json
{
  "texts": ["Document 1 text...", "Document 2 text..."]
}
```
✅ Returns: number of stored nodes

---

## 💬 POST /generate
**Ask a question based on stored documents**
```json
{
  "new_message": {
    "role": "user",
    "content": "What is the capital of France?"
  }
}
```
✅ Returns: answer + relevant contexts

---

## 📡 GET /
**API Status Check**
Returns a simple confirmation message.

---

## 🧼 Cleanup Vector DB
To remove the vector store:
```bash
rm -rf vector_store/chroma.db
```

---

## 🧠 Notes
- Embedding service runs `BAAI/bge-small-en` via FastAPI.
- Ollama must pull the model before first use:
```bash
ollama pull qwen:0.5b
```

---

## ✅ Requirements Met
- ✅ CPU-only deployment (no GPU)
- ✅ RAM under 16GB
- ✅ Dockerized (3 containers)
- ✅ Compliant API format
- ✅ Modular & scalable

---

## 🧪 Example Query
```bash
curl -X POST http://localhost:8000/generate \
 -H 'Content-Type: application/json' \
 -d '{
   "new_message": {"role": "user", "content": "Explain photosynthesis."}
 }'
```
