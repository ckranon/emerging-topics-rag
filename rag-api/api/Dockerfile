# rag_api/api/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY api_rag.py ./

CMD ["uvicorn", "api_rag:app", "--host", "0.0.0.0", "--port", "8000"]