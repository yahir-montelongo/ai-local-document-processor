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

### 2. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto (basado en el archivo `.env.example`) y define tu clave secreta para la API:

```env
API_KEY=tu_clave_secreta_aqui
```
*(Nota: El archivo `.env` está en el `.gitignore` para proteger tus credenciales).*

### 3. Descargar el modelo en Ollama
Abre tu terminal y descarga el modelo base necesario:

```bash
ollama run llama3.2
```

*(Una vez descargado, puedes salir escribiendo `/bye`).*

### 4. Levantar los servicios con Docker
Ejecuta el siguiente comando para compilar y arrancar el contenedor de FastAPI configurado para comunicarse con tu host local:

```bash
docker compose up --build
```

---

## Uso de la API

Una vez que el servidor esté activo, puedes acceder a la documentación interactiva (Swagger UI) en tu navegador:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

### Endpoint principal: `POST /api/v1/query`

> **Seguridad:** Este endpoint requiere autenticación. Debes enviar la cabecera `X-API-Key` con el valor definido en tu archivo `.env`.

**Ejemplo de petición:**

```json
{
  "document_text": "La empresa TecnoSoluciones fue fundada en 2015 en Guadalajara. Su horario de atención es de lunes a viernes de 9:00 a 18:00 horas.",
  "question": "¿Cuál es el horario de atención de la empresa?"
}
```

**Respuesta exitosa (200):**

```json
{
  "status": "success",
  "answer": "El horario de atención es de lunes a viernes de 9:00 a 18:00 horas."
}
```

#### Ejemplo usando `curl`:

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_clave_secreta_aqui" \
  -d '{
    "document_text": "FastAPI es un framework de Python.",
    "question": "¿Qué es FastAPI?"
  }'
```

---

## Pruebas Automatizadas

El proyecto cuenta con una suite de pruebas (pytest) que cubren validaciones de entrada, construcción del prompt, manejo de errores de Ollama (502, 503, 504) y la seguridad de la API (403).

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