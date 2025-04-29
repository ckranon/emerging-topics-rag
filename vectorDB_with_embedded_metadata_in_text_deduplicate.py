import json
import re
import uuid
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma

# 📂 Configuración fija
jsonl_path = "chunks_normas_final_with_ids.jsonl"
persist_dir = "chroma_db_normas_completo"
batch_size = 2000
modelo = "dariolopez/bge-m3-es-legal-tmp-3"

# 🛠️ Incrustar metadatos en el texto
def mejorar_texto_completo(item: dict) -> str:
    meta = item["metadata"]
    articulo_normalizado = re.sub(r'[^a-zA-Z0-9\s]', '', meta.get("articulo", ""))
    return "\n".join([
        f"[TIPO] {meta.get('tipo', '')}",
        f"[NUMERO] {meta.get('numero', '')}",
        f"[SECTOR] {meta.get('sector', '')}",
        f"[FECHA] {meta.get('fecha', '')}",
        f"[SUMILLA] {meta.get('sumilla', '')}",
        f"[ARTICULO] {articulo_normalizado}",
        f"[LIBRO] {meta.get('libro', '')}",
        f"[DISPOSICION] {meta.get('disposicion', '')}",
        f"[TITULO] {meta.get('titulo', '')}",
        f"[CAPITULO] {meta.get('capitulo', '')}",
        f"[REFERENCIA] {meta.get('referencia', '')}",
        f"[LINK] {meta.get('link', '')}",
        "",
        item["text"]
    ])

# 📥 Cargar chunks
with open(jsonl_path, "r", encoding="utf-8") as f:
    docs_raw = [json.loads(line) for line in f]

# 🧠 Modelo de embeddings
model = SentenceTransformer(modelo, device="cpu")

# 🧱 Cargar Chroma existente
chroma_db = Chroma(
    persist_directory=persist_dir,
    embedding_function=None
)

# Obtener IDs existentes
existing = chroma_db.get()
existing_ids = set(existing["ids"])
print(f"📦 Chroma contiene actualmente {len(existing_ids)} documentos.")

# 🔁 Preparar nuevos chunks
new_ids, new_texts, new_embeddings, new_metadatas = [], [], [], []

for item in tqdm(docs_raw, desc="🔎 Evaluando documentos"):
    uid = str(uuid.uuid4())
    while uid in existing_ids:
        uid = str(uuid.uuid4())  # asegurar que no haya colisión (casi imposible)

    enriched_text = mejorar_texto_completo(item)
    embedding = model.encode(enriched_text, normalize_embeddings=True)

    new_ids.append(uid)
    new_texts.append(enriched_text)
    new_embeddings.append(embedding)
    new_metadatas.append(item["metadata"])

print(f"🆕 Documentos nuevos a insertar: {len(new_ids)}")

# 📦 Insertar en Chroma
for i in tqdm(range(0, len(new_ids), batch_size), desc="📡 Indexando en Chroma"):
    chroma_db._collection.add(
        ids=new_ids[i:i+batch_size],
        embeddings=new_embeddings[i:i+batch_size],
        documents=new_texts[i:i+batch_size],
        metadatas=new_metadatas[i:i+batch_size]
    )

chroma_db.persist()
print("✅ Base vectorial con UUIDs única y completamente actualizada.")
