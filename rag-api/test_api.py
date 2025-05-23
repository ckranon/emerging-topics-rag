
#!/usr/bin/env python3
"""
Standalone test script to upload documents, generate responses, build a dataset,
and embed hard‑coded ground truths for later evaluation with Ragas metrics.
"""
import time
import requests
from datasets import Dataset
import time
import requests
import ragas.metrics as rmetrics


# Configuration
BASE_URL = "http://localhost:8000"
FALLBACK_LOG = "fallback_records.jsonl"


# 0. Hard‑coded documents
TEST_TEXTS = [
    """
Bolivia, oficialmente el Estado Plurinacional de Bolivia (en quechua: Puliwya Achka Aylluska Mamallaqta; en aimara: Wuliwya Walja Ayllunakana Marka; en guaraní: Tetã Hetate'ýigua Mborívia), es un país soberano ubicado en la región centro occidental de América del Sur, miembro de la Comunidad Andina, constituido políticamente como un Estado social plurinacional, unitario, descentralizado y con autonomías. El país está organizado en nueve departamentos, ciento doce provincias y una región autónoma. La capital oficial es Sucre, que alberga al órgano judicial, mientras que la sede de Gobierno es la ciudad de La Paz, que ejerce como capital de facto y que alberga a los órganos ejecutivo, legislativo y electoral. La ciudad más poblada es Santa Cruz de la Sierra.

Limita al norte y este con Brasil; al sur con Paraguay y Argentina; y al oeste con Chile y Perú. Es considerado un Estado sin litoral y constitucionalmente mantiene una reclamación territorial a Chile por una salida soberana al océano Pacífico. Sin embargo, tiene un enclave en Perú al sur del puerto de Ilo, denominado Bolivia Mar, consistente en una playa sobre la costa del Pacífico de cinco kilómetros de largo por un kilómetro de ancho de superficie.
""",
    """
España, formalmente el Reino de España, es un país soberano transcontinental, constituido en Estado social y democrático de derecho y cuya forma de gobierno es la monarquía parlamentaria. ... Concretamente, a 1 de julio de 2024 llegó hasta los 48 797 897.
""",
    """
Francia (en francés: France), oficialmente la República Francesa (République française), es un país soberano transcontinental... Sus dieciocho regiones integrales (cinco de las cuales son de ultramar) abarcan una superficie combinada de 643 801 km2 y más de 68 millones de personas.
""",
]

# 1. Questions and hard‑coded ground truths
QUESTIONS = [
    "¿Cuál es la capital oficial de Bolivia y qué órgano alberga?",
    "¿En cuántos departamentos está organizado políticamente Bolivia?",
    "¿Qué reclamación territorial mantiene Bolivia y cómo se llama su enclave en Perú?",
    "¿Cuál es la forma de gobierno de España según su Constitución?",
    "¿Cuántas comunidades autónomas y cuántas provincias forman España?",
    "¿Qué población tenía España al 1 de julio de 2024?",
    "¿Cómo se define la forma de gobierno de la República Francesa y cuál es su capital?",
    "¿Cuántas regiones integrales tiene Francia y cuántas de ellas son de ultramar?",
    "¿Cuál es la superficie combinada de las regiones de Francia y su población aproximada?",
]
GROUND_TRUTHS = [
    "La capital oficial es Sucre, que alberga al órgano judicial.",
    "Nueve departamentos.",
    "Reclamación territorial a Chile por salida soberana al océano Pacífico; su enclave en Perú se denomina 'Bolivia Mar'.",
    "Monarquía parlamentaria.",
    "Diecisiete comunidades autónomas y cincuenta provincias.",
    "48 797 897 habitantes.",
    "República semipresidencialista unitaria, con capital en París.",
    "Dieciocho regiones integrales, cinco de ellas de ultramar.",
    "Una superficie de 643 801 km² y más de 68 millones de personas.",
]


def status_check():
    try:
        res = requests.get(f"{BASE_URL}/")
        res.raise_for_status()
        print("Status Check:", res.json())
    except Exception as e:
        print(f"RAG API unreachable: {e}")
        exit(1)


def upload_documents(texts):
    res = requests.post(f"{BASE_URL}/upload", json={"texts": texts})
    res.raise_for_status()
    print("Upload Response:", res.json())


def generate_and_time(questions):
    times, results = [], []
    for q in questions:
        start = time.time()
        resp = requests.post(
            f"{BASE_URL}/generate",
            json={"new_message": {"role": "user", "content": q}}
        )
        elapsed = time.time() - start
        resp.raise_for_status()
        data = resp.json()
        text = data.get("output") or data.get("generated_text", "")
        ctxs = data.get("contexts", [])
        times.append(elapsed)
        results.append((text, ctxs))
        print(f"Q: {q}\nA: {text}\nTime: {elapsed:.3f}s\nContexts: {ctxs}\n")

    avg_time = sum(times) / len(times)
    with open("avg_time.txt", "w", encoding="utf-8") as f:
        f.write(f"{avg_time:.3f}\n")
    print(f"Avg time: {avg_time:.3f}s (written to avg_time.txt)")
    return results


def main():
    status_check()
    print("Uploading documents...")
    upload_documents(TEST_TEXTS)

    print("Generating responses...")
    results = generate_and_time(QUESTIONS)

    # Build dataset with query, response, contexts, and ground truth
    generated = [resp for resp, _ in results]
    contexts = [ctxs for _, ctxs in results]
    data = {
        "user_input": QUESTIONS,
        "response": generated,
        "retrieved_contexts": contexts,
        "reference": GROUND_TRUTHS,
    }
    dataset = Dataset.from_dict(data)
    # Save dataset for later evaluation steps
    out_dir = "eval_dataset_with_gt"
    dataset.save_to_disk(out_dir)
    print(f"Saved augmented dataset ({len(dataset)} rows) to '{out_dir}'.")

if __name__ == "__main__":
    main()

