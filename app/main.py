import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

app = FastAPI(title="AI Document Processor", version="1.0")


class QueryRequest(BaseModel):
    document_text: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)


class QueryResponse(BaseModel):
    status: str
    answer: str


@app.post("/api/v1/query", response_model=QueryResponse)
def process_document_query(payload: QueryRequest):
    prompt = (
        "Responde únicamente con la información del documento. "
        "Si la respuesta no está en el documento, di que no se encuentra.\n\n"
        f"Documento:\n{payload.document_text}\n\n"
        f"Pregunta: {payload.question}"
    )
    body = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}

    try:
        response = requests.post(OLLAMA_URL, json=body, timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "No se pudo conectar con Ollama. Verifica que esté abierto.")
    except requests.exceptions.Timeout:
        raise HTTPException(504, "Ollama tardó demasiado en responder.")
    except requests.exceptions.HTTPError:
        raise HTTPException(502, f"Error en Ollama: {response.text}")

    answer = response.json().get("response", "").strip()
    return QueryResponse(status="success", answer=answer or "Sin respuesta.")
