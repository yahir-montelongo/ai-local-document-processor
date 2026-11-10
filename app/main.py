import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Document Processor", version="1.0")

class QueryRequest(BaseModel):
    document_text: str
    question: str

@app.post("/api/v1/query")
async def process_document_query(payload: QueryRequest):
    prompt = f"Basándote en el documento:\n\n{payload.document_text}\n\nResponde: {payload.question}"
    
    # URL para que Docker se comunique con Ollama en tu equipo Windows
    ollama_url = "http://host.docker.internal:11434/api/generate"
    
    body = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(ollama_url, json=body, timeout=60)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Error en Ollama: {response.text}")
            
        result = response.json()
        return {
            "status": "success",
            "answer": result.get("response", "Sin respuesta.")
        }
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500, 
            detail="No se pudo conectar con Ollama. Asegúrate de que Ollama esté abierto en tu PC."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))