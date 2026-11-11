# AI Local Document Processor

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

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

```bash
git clone https://github.com/yahir-montelongo/ai-local-document-processor.git
cd ai-local-document-processor
```

### 2. Descargar el modelo en Ollama
Abre tu terminal y descarga el modelo base necesario:

```bash
ollama run llama3.2
```

*(Una vez descargado, puedes salir escribiendo `/bye`).*

### 3. Levantar los servicios con Docker
Ejecuta el siguiente comando para compilar y arrancar el contenedor de FastAPI configurado para comunicarse con tu host local:

```bash
docker compose up --build
```

---

## Uso de la API

Una vez que el servidor esté activo, puedes acceder a la documentación interactiva (Swagger UI) en tu navegador:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

### Endpoint principal: `POST /api/v1/query`
Envía una petición con el texto del documento y la pregunta que deseas resolver:

```json
{
  "document_text": "Los sistemas de gestión se conectan mediante APIs REST y FastAPI.",
  "question": "¿Qué tecnologías se usan para conectar los sistemas?"
}
```

**Respuesta exitosa (200):**

```json
{
  "status": "success",
  "answer": "Según el documento, los sistemas se conectan mediante APIs REST y FastAPI."
}
```

---

## Pruebas Automatizadas

El proyecto cuenta con una suite de pruebas (pytest) que cubren validaciones de entrada, construcción del prompt y manejo de errores de Ollama (502, 503, 504).

Para ejecutarlas localmente (sin necesidad de tener Ollama corriendo, ya que se usa `monkeypatch`):

```bash
pip install -r requirements-dev.txt
pytest -v
```

---

## Privacidad

Este proyecto procesa toda la información de forma local con Ollama. Los documentos y las preguntas nunca se envían a servicios externos.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.