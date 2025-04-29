# semantic_chunk_batch.py

import os
import glob
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import numpy as np
import nltk

# Download Spanish punkt tokenizer
nltk.download('punkt')

# --- CONFIGURATION ---
CHROMA_DIR = "chroma"
EMBEDDING_MODEL_NAME = "sentence-transformers/static-similarity-mrl-multilingual-v1"
SIMILARITY_THRESHOLD = 0.80  # Cosine similarity to continue a chunk
MAX_SENTENCES_PER_CHUNK = 8
MIN_SENTENCES_PER_CHUNK = 2

# --- Initialize ChromaDB ---
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=CHROMA_DIR
))
collection = client.get_or_create_collection(name="spanish_chunks")

# --- Load Embedding Model ---
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# --- Functions ---

def split_into_sentences(text):
    """Splits Spanish text into sentences."""
    from nltk.tokenize import sent_tokenize
    return sent_tokenize(text, language='spanish')

def cosine_similarity(a, b):
    """Computes cosine similarity between two vectors."""
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    return np.dot(a_norm, b_norm)

def semantic_chunk(sentences, embeddings, threshold=SIMILARITY_THRESHOLD):
    """Groups sentences based on vector semantic similarity."""
    chunks = []
    current_chunk = [sentences[0]]
    last_embedding = embeddings[0]

    for sent, embed in zip(sentences[1:], embeddings[1:]):
        sim = cosine_similarity(last_embedding, embed)

        if sim >= threshold and len(current_chunk) < MAX_SENTENCES_PER_CHUNK:
            current_chunk.append(sent)
        else:
            if len(current_chunk) >= MIN_SENTENCES_PER_CHUNK:
                chunks.append(' '.join(current_chunk))
            else:
                if chunks:
                    chunks[-1] += ' ' + ' '.join(current_chunk)
                else:
                    chunks.append(' '.join(current_chunk))
            current_chunk = [sent]
        last_embedding = embed

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def embed_texts(texts):
    """Embeds a list of texts."""
    return model.encode(texts, show_progress_bar=True)

def store_chunks_in_chroma(chunks, file_name):
    """Stores chunks with metadata into ChromaDB."""
    embeddings = embed_texts([chunk['text'] for chunk in chunks]).tolist()
    ids = [chunk['id'] for chunk in chunks]
    metadatas = [{'source_file': chunk['file_name']} for chunk in chunks]

    collection.add(
        documents=[chunk['text'] for chunk in chunks],
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    client.persist()

def process_text_file(file_path):
    """Processes a single text file into semantic chunks."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = split_into_sentences(text)
    if len(sentences) < 2:
        return []  # skip if too short

    embeddings = embed_texts(sentences)
    semantic_chunks = semantic_chunk(sentences, embeddings)

    chunks_with_metadata = []
    for chunk_text in semantic_chunks:
        chunks_with_metadata.append({
            'id': str(uuid.uuid4()),
            'file_name': os.path.basename(file_path),
            'text': chunk_text
        })

    return chunks_with_metadata

def process_folder(folder_path):
    """Processes all .txt files in a folder."""
    all_chunks = []
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    for file_path in txt_files:
        print(f"Processing: {file_path}")
        chunks = process_text_file(file_path)
        if chunks:
            store_chunks_in_chroma(chunks, os.path.basename(file_path))
            all_chunks.extend(chunks)

    print(f"Total {len(all_chunks)} semantic chunks stored from {len(txt_files)} files.")

# --- Example Usage ---

if __name__ == "__main__":
    FOLDER_TO_PROCESS = "input_texts"  # replace with your folder
    if os.path.exists(FOLDER_TO_PROCESS):
        process_folder(FOLDER_TO_PROCESS)
    else:
        print(f"Folder {FOLDER_TO_PROCESS} not found.")
