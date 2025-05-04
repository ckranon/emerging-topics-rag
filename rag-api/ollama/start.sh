#!/bin/sh

# Background: wait a few seconds, then pull the model if it's not already there
(
  sleep 5
  if ! ollama list | grep -q "qwen2.5:0.5b"; then
    echo "[INFO] Pulling qwen2.5:0.5b..."
    ollama pull qwen2.5:0.5b
  else
    echo "[INFO] qwen2.5:0.5b already present."
  fi
) &

# Foreground: start the Ollama server
echo "[INFO] Starting Ollama server..."
exec ollama serve
