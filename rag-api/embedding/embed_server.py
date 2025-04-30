from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
import uvicorn

app = FastAPI()
model = SentenceTransformer("sentence-transformers/static-similarity-mrl-multilingual-v1") # <- SPANISH!
# model = SentenceTransformer("BAAI/bge-small-en") # <- ENGLISH!

@app.post("/embed")
async def embed(request: Request):
    data = await request.json()
    texts = data.get("texts", [])
    vectors = model.encode(texts, normalize_embeddings=True).tolist()
    return {"vectors": vectors}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
