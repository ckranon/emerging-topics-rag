#!/bin/sh

# Background: wait a few seconds, then pull the model if it's not already there
(
  sleep 5
  if ! ollama list | grep -q "deepseek-r1:1.5b"; then
    echo "[INFO] Pulling deepseek-r1:1.5b..."
    ollama pull deepseek-r1:1.5b
  else
    echo "[INFO] Model already present."
  fi
) &

# Foreground: start the Ollama server
echo "[INFO] Starting Ollama server..."
exec ollama serve
