import logging
import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger("document_processor")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "4096"))
MAX_DOCUMENT_CHARS = int(os.getenv("MAX_DOCUMENT_CHARS", "50000"))

app = FastAPI(title="AI Document Processor", version="1.1")


class QueryRequest(BaseModel):
    document_text: str = Field(..., min_length=1, max_length=MAX_DOCUMENT_CHARS)
    question: str = Field(..., min_length=1, max_length=2000)


class QueryResponse(BaseModel):
    status: str
    answer: str


@app.get("/health")
def health():
    """Comprueba que la API está viva (no valida la conexión con Ollama)."""
    return {"status": "ok"}


@app.post("/api/v1/query", response_model=QueryResponse)
def process_document_query(payload: QueryRequest):
    prompt = (
        "Responde únicamente con la información del documento. "
        "Si la respuesta no está en el documento, di que no se encuentra.\n\n"
        f"Documento:\n{payload.document_text}\n\n"
        f"Pregunta: {payload.question}"
    )
    body = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": OLLAMA_NUM_CTX},
    }

    try:
        response = requests.post(OLLAMA_URL, json=body, timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        logger.error("No se pudo conectar con Ollama en %s", OLLAMA_URL)
        raise HTTPException(503, "No se pudo conectar con Ollama. Verifica que esté abierto.")
    except requests.exceptions.Timeout:
        logger.error("Timeout esperando a Ollama (%s s)", OLLAMA_TIMEOUT)
        raise HTTPException(504, "Ollama tardó demasiado en responder.")
    except requests.exceptions.HTTPError as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        logger.error("Ollama respondió con error: %s", detail)
        raise HTTPException(502, f"Error en Ollama: {detail}")
    except (requests.exceptions.RequestException, ValueError):
        logger.exception("Respuesta inválida o error de red con Ollama")
        raise HTTPException(502, "Respuesta inválida de Ollama.")

    answer = str(data.get("response", "")).strip()
    return QueryResponse(status="success", answer=answer or "Sin respuesta.")
