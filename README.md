# AI Local Document Processor

API REST desarrollada con FastAPI y Docker que responde preguntas sobre un documento usando un modelo de lenguaje local (Llama 3.2 3B mediante Ollama). Todo el procesamiento ocurre en tu equipo: ningún dato sale hacia servidores de terceros.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
| :--- | :--- |
| **Backend** | Python, FastAPI, Pydantic, Requests |
| **IA Local** | Ollama (`llama3.2`, 3B parámetros) |
| **Contenedores** | Docker y Docker Compose |

---

## ⚙️ Cómo Funciona

```text
Cliente ──► FastAPI (contenedor) ──► Ollama (tu equipo, puerto 11434) ──► Llama 3.2
   ◄────────────── respuesta JSON ◄──────────────┘
La API arma un prompt que obliga al modelo a responder solo con la información del documento. Si la respuesta no está en el texto, el modelo indica que no se encuentra.   📋 Requisitos PreviosDocker y Docker Compose instalados.   Ollama instalado y corriendo en tu máquina.   🚀 Puesta en Marcha1. Clonar el repositorioBashgit clone [https://github.com/yahir-montelongo/ai-local-document-processor.git](https://github.com/yahir-montelongo/ai-local-document-processor.git)
cd ai-local-document-processor
2. Descargar el modeloDescarga el modelo base en tu equipo:Bashollama pull llama3.2
Nota para usuarios de Linux: Por defecto Ollama solo escucha en 127.0.0.1 y el contenedor no podrá alcanzarlo. Inicia Ollama configurando la variable de red: OLLAMA_HOST=0.0.0.0 ollama serve. En Windows y macOS con Docker Desktop no hace falta ningún ajuste adicional.   3. Levantar el servicio con DockerBashdocker compose up --build -d
🔌 Uso de la APILa documentación interactiva (Swagger UI) queda disponible en http://localhost:8000/docs.   Endpoint: POST /api/v1/queryPetición (JSON):JSON{
  "document_text": "Los sistemas de gestión se conectan mediante APIs REST y FastAPI.",
  "question": "¿Qué tecnologías se usan para conectar los sistemas?"
}
Respuesta exitosa (200):JSON{
  "status": "success",
  "answer": "Según el documento, los sistemas se conectan mediante APIs REST y FastAPI."
}
⚠️ Códigos de ErrorCódigoCausa probable422Campos vacíos o faltantes en la petición   502Ollama respondió con un error   503No se pudo conectar con Ollama (verifica que esté abierto)   504Ollama tardó más del tiempo límite en responder   ⚙️ Configuración (Variables de Entorno)Se definen directamente en el archivo docker-compose.yml:   OLLAMA_URL: Endpoint de Ollama (por defecto: http://host.docker.internal:11434/api/generate)[cite: 2].OLLAMA_MODEL: Modelo a utilizar (por defecto: llama3.2)[cite: 2].OLLAMA_TIMEOUT: Tiempo límite en segundos (por defecto: 120)[cite: 2].🛡️ PrivacidadEste proyecto procesa toda la información de forma local con Ollama. Los documentos y las preguntas nunca se envían a servicios externos[cite: 2].
