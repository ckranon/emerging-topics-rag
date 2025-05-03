# rag_api/embedding/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY embed_server.py ./

CMD ["uvicorn", "embed_server:app", "--host", "0.0.0.0", "--port", "8001"]