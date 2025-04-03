import requests
import difflib

def similarity_score(text1, text2):
    """Compute a similarity ratio between two strings (case insensitive)."""
    return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def evaluate_ragas(question, answer, contexts, reference):
    """Compute simple RAGAS-like metrics."""
    combined_context = " ".join(contexts) if contexts else ""
    metrics = {}
    
    metrics["Answer Similarity"] = similarity_score(answer, reference)
    metrics["Answer Correctness"] = 1 if reference.lower() in answer.lower() else 0
    metrics["Faithfulness"] = similarity_score(answer, combined_context) if combined_context else 0
    metrics["Answer Relevancy"] = similarity_score(answer, question)
    
    answer_tokens = set(answer.lower().split())
    context_tokens = set(combined_context.lower().split())
    common_tokens = answer_tokens.intersection(context_tokens)
    
    metrics["Context Precision"] = len(common_tokens) / len(answer_tokens) if answer_tokens else 0
    metrics["Context Utilization"] = len(common_tokens) / len(context_tokens) if context_tokens else 0
    metrics["Context Recall"] = metrics["Context Precision"]  # Basic fallback for now
    
    return metrics

def main():
    base_url = "http://localhost:8000"  # Adjust if needed
# Upload sample texts
    texts = [
        "The capital of France is Paris. France is in Europe.",
        "Don Quixote was written by Miguel de Cervantes in the early 17th century.",
        "Python is a popular programming language created by Guido van Rossum."
    ]
    upload_payload = {"texts": texts}
    print("Uploading documents...\n")
    resp_upload = requests.post(f"{base_url}/upload", json=upload_payload)
    print("Status code /upload:", resp_upload.status_code)
    print("Response /upload:", resp_upload.json())

    # Example questions and expected (reference) answers for evaluation
    questions = [
        "What is the capital of France?",
        "Who created the Python language?",
        "Who wrote Don Quixote?"
    ]
    expected_answers = {
        "What is the capital of France?": "Paris",
        "Who created the Python language?": "Guido van Rossum",
        "Who wrote Don Quixote?": "Miguel de Cervantes"
    }

    for q in questions:
        print(f"\nQuestion: {q}")
        generate_payload = {"new_message": {"role": "user", "content": q}}
        resp_generate = requests.post(f"{base_url}/generate", json=generate_payload)
        print("Status code /generate:", resp_generate.status_code)
        if resp_generate.ok:
            data = resp_generate.json()
            generated_answer = data.get("generated_text", "")
            response_time = data.get("timing")
            # Ensure we have contexts as a list (if not present, default to empty list)
            contexts = data.get("contexts", [])
            print("Generated response:", generated_answer)
            print("Response time:", response_time)
            print("Retrieved contexts:", contexts)
            
            # Evaluate using RAGAS metrics
            ref_answer = expected_answers.get(q, "")
            metrics = evaluate_ragas(q, generated_answer, contexts, ref_answer)
            print("\nRAGAS Metrics:")
            for metric, value in metrics.items():
                print(f"  {metric}: {value:.2f}")
        else:
            print("Error:", resp_generate.text)

if __name__ == "__main__":
    main()

