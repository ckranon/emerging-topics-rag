import time
import requests
import ragas.metrics as rmetrics

BASE_URL = "http://localhost:8000"

# 1. Status check
def status_check():
    res = requests.get(f"{BASE_URL}/")
    print("Status Check:", res.json())

### TODO: FIND A WAY TO ADD TEXTS BASED ON FOLDER #####


# 2. Generate three Spanish documents of exactly 5000 characters each
def generate_spanish_docs(count=3, length=5000):
    base_text = (
        "La inteligencia artificial ha transformado muchas industrias, desde la salud hasta la educación. "
        "Mediante el uso de algoritmos avanzados y aprendizaje automático, se pueden generar soluciones "
        "innovadoras que mejoran la eficiencia y la calidad de los servicios. Además, los avances en "
        "procesamiento de lenguaje natural han permitido una comunicación más fluida entre humanos y máquinas. "
        "La combinación de grandes volúmenes de datos y potentes capacidades de cómputo ha llevado al desarrollo "
        "de modelos que superan los límites de lo que era posible hace solo unos años."
    )
    docs = []
    repeats = (length // len(base_text)) + 2
    long_text = base_text * repeats
    for _ in range(count):
        docs.append(long_text[:length])
    return docs

# 3. Upload documents and questions
def upload_documents_and_questions():
    docs = generate_spanish_docs()
    payload = {"texts": docs}
    res = requests.post(f"{BASE_URL}/upload", json=payload)
    print("Upload Response:", res.json())

    questions = [
        "¿Cómo ha influido la inteligencia artificial en la mejora de la calidad de los servicios?",
        "¿Qué papel juega el procesamiento de lenguaje natural en la comunicación entre humanos y máquinas?",
        "¿Cuáles son los requisitos clave para el desarrollo de modelos avanzados de inteligencia artificial?"
    ]
    return questions

# 4. Generate answers and measure response times
def generate_and_time(questions):
    times = []
    responses = []
    for q in questions:
        payload = {"new_message": {"role": "user", "content": q}}
        start = time.time()
        res = requests.post(f"{BASE_URL}/generate", json=payload)
        elapsed = time.time() - start
        times.append(elapsed)
        resp_json = res.json()
        responses.append(resp_json)
        print(f"Question: {q}\nResponse: {resp_json}\nTime: {elapsed:.3f}s\n")
    avg_time = sum(times) / len(times)
    print(f"Average Response Time: {avg_time:.3f}s")
    return avg_time, responses

# 5. Evaluate RAGAS metrics using ragas.metrics package
def evaluate_ragas_metrics(questions, responses):
    # Extract response texts from API output
    response_texts = []
    for r in responses:
        # Adjust key based on your generate endpoint output
        text = r.get('output') or r.get('generated_text') or r.get('response', '')
        response_texts.append(text)

    metrics_list = [
        'Faithfulness',
        'Answer Relevancy',
        'Answer Correctness',
        'Context Precision',
        'Context Utilization',
        'Context Recall',
        'Answer Similarity'
    ]

    # Compute metrics locally
    metrics = rmetrics.compute_metrics(
        queries=questions,
        responses=response_texts,
        metrics=metrics_list
    )

    print("RAGAS Metrics:")
    for name in metrics_list:
        val = metrics.get(name)
        print(f"- {name}: {val:.2f}")
    return metrics

if __name__ == "__main__":
    status_check()
    questions = upload_documents_and_questions()
    avg_time, responses = generate_and_time(questions)
    ragas = evaluate_ragas_metrics(questions, responses)
