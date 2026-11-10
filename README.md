# AI Local Document Processor

API desarrollada con **FastAPI**, **Docker** y modelos de lenguaje locales ejecutados mediante **Ollama** (`llama3.2`), diseñada para procesar y responder consultas sobre documentos de forma completamente local y privada.

## Stack Tecnológico
* **Backend:** Python, FastAPI, Pydantic, Requests
* **IA Local:** Ollama (Llama 3.2 3B)
* **Contenedorización:** Docker & Docker Compose

---

## Requisitos Previos
Asegúrate de tener instalado en tu equipo:
* [Docker y Docker Compose](https://www.docker.com/)
* [Ollama](https://ollama.com/) corriendo en tu máquina local.

---

## Configuración y Puesta en Marcha

Sigue estos pasos para clonar y echar a andar el proyecto en tu entorno local:

### 1. Clonar el repositorio
\`\`\`bash
git clone https://github.com/yahir-montelongo/ai-local-document-processor.git
cd ai-local-document-processor
\`\`\`

### 2. Descargar el modelo en Ollama
Abre tu terminal y descarga el modelo base necesario:
\`\`\`bash
ollama run llama3.2
\`\`\`
*(Una vez descargado, puedes salir escribiendo `/bye`).*

### 3. Levantar los servicios con Docker
Ejecuta el siguiente comando para compilar y arrancar el contenedor de FastAPI configurado para comunicarse con tu host local:
\`\`\`bash
docker compose up --build
\`\`\`

---

## Uso de la API

Una vez que el servidor esté activo, puedes acceder a la documentación interactiva (Swagger UI) en tu navegador:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

### Endpoint principal: `POST /api/v1/query`
Envía una petición con el texto del documento y la pregunta que deseas resolver:

**Ejemplo de Payload (JSON):**
\`\`\`json
{
  "document_text": "Los sistemas de gestión se conectan mediante APIs REST y FastAPI.",
  "question": "¿Qué tecnologías se usan para conectar los sistemas?"
}
\`\`\`

**Ejemplo de Respuesta:**
\`\`\`json
{
  "status": "success",
  "answer": "Según el documento, los sistemas se conectan mediante APIs REST y FastAPI."
}
\`\`\`

---

## 🛡️ Privacidad
Este proyecto procesa toda la información de manera local utilizando Ollama, garantizando que ningún dato de tus documentos salga hacia servidores de terceros.
