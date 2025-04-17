# rag_api/api/api_rag.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import requests
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.core.node_parser import SentenceWindowNodeParser
import os

app = FastAPI()

CHROMA_DIR = "../vector_store/chroma.db"
EMBEDDING_URL = "http://embedding:8001/embed"
OLLAMA_URL = "http://llm:11434/api/generate"

db_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = db_client.get_or_create_collection("rag_collection")
node_parser = SentenceWindowNodeParser.from_defaults()

class UploadRequest(BaseModel):
    texts: List[str]

class GenerateRequest(BaseModel):
    new_message: dict

@app.get("/")
def status():
    return {"message": "RAG API is running successfully"}

@app.post("/upload")
def upload_docs(req: UploadRequest):
    all_nodes = []
    for text in req.texts:
        nodes = node_parser.get_nodes_from_documents([Document(text=text)])
        all_nodes.extend(nodes)

    chunks = [node.text for node in all_nodes]
    res = requests.post(EMBEDDING_URL, json={"texts": chunks})
    vectors = res.json()["vectors"]

    ids = [f"doc_{i}" for i in range(len(vectors))]
    collection.add(documents=chunks, embeddings=vectors, ids=ids)

    return {"message": "Vector index successfully created", "nodes_count": len(chunks)}

@app.post("/generate")
def generate(req: GenerateRequest):
    query = req.new_message["content"]
    res = requests.post(EMBEDDING_URL, json={"texts": [query]})
    query_vec = res.json()["vectors"][0]

    results = collection.query(query_embeddings=[query_vec], n_results=3)
    contexts = results["documents"][0]

    prompt = (
    "You are a helpful assistant. Use the context below to answer the user's question.\n\n"
    f"Context:\n{chr(10).join(contexts)}\n\n"
    f"Question: {query}\nAnswer:")

    gen_response = requests.post(OLLAMA_URL, json={"model": "qwen2.5:0.5b", "prompt": prompt, "stream": False})
    answer = gen_response.json().get("response", "")

    return {"generated_text": answer, "contexts": contexts}