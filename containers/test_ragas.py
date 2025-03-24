import requests
import datasets
from ragas import evaluate
from ragas.metrics import context_precision, faithfulness, answer_relevancy, context_recall

def main():
    base_url = "http://localhost:8000"  # Adjust if needed

    # Step 1: Upload sample documents to your RAG system
    texts = [
        "The capital of France is Paris. France is in Europe.",
        "Don Quixote was written by Miguel de Cervantes in the early 17th century.",
        "Python is a popular programming language created by Guido van Rossum."
    ]
    upload_payload = {"texts": texts}
    print("Uploading documents...")
    resp_upload = requests.post(f"{base_url}/upload", json=upload_payload)
    print("Upload response:", resp_upload.json())

    # Step 2: Ask a few questions and collect generated answers
    questions = [
        "What is the capital of France?",
        "Who created the Python language?",
        "Who wrote Don Quixote?"
    ]
    
    references = [
        "The capital of France is Paris.",
        "Guido van Rossum created the Python language.",
        "Miguel de Cervantes wrote Don Quixote."
    ]
    
    eval_records = []
    for q, ref in zip(questions, references):
        print(f"\nQuestion: {q}")
        generate_payload = {"new_message": {"role": "user", "content": q}}
        resp_generate = requests.post(f"{base_url}/generate", json=generate_payload)
        if resp_generate.ok:
            data = resp_generate.json()
            generated_text = data.get("generated_text", "")
            print("Generated response:", generated_text)
        else:
            generated_text = ""
            print("Error:", resp_generate.text)
        
        # Here, we create a record with the question, generated answer, reference, and an empty context.
        record = {
            "question": q,
            "answer": generated_text,
            "reference": ref,  # Add reference column for evaluation
            "contexts": []  # Replace with actual contexts if available
        }
        eval_records.append(record)

    # Step 3: Convert evaluation records into a Dataset object (from Hugging Face datasets)
    dataset = datasets.Dataset.from_list(eval_records)

    # Step 4: Use Ragas to evaluate your RAG pipeline responses using selected metrics.
    # You can choose from many metrics—here we use context_precision, faithfulness,
    # answer_relevancy, and context_recall.
    print("\nEvaluating with Ragas metrics...")
    metrics_result = evaluate(dataset, metrics=[context_precision, faithfulness, answer_relevancy, context_recall])
    print("\nEvaluation Metrics:")
    print(metrics_result)

if _name_ == "_main_":
    main()
