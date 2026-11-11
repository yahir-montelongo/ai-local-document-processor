from unittest.mock import MagicMock

import pytest
import requests
from fastapi.testclient import TestClient

from app.main import API_KEY, MAX_DOCUMENT_CHARS, app

client = TestClient(app, headers={"X-API-Key": API_KEY})

URL = "/api/v1/query"
PAYLOAD = {
    "document_text": "FastAPI es un framework web de Python.",
    "question": "¿Qué es FastAPI?",
}


def _ollama_ok(text="Un framework web de Python."):
    resp = MagicMock()
    resp.raise_for_status.return_value = None
    resp.json.return_value = {"response": text}
    return resp


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_query_ok(monkeypatch):
    monkeypatch.setattr("app.main.requests.post", lambda *a, **k: _ollama_ok())
    r = client.post(URL, json=PAYLOAD)
    assert r.status_code == 200
    assert r.json() == {"status": "success", "answer": "Un framework web de Python."}


def test_prompt_enviado_a_ollama(monkeypatch):
    captured = {}

    def fake_post(url, json, timeout):
        captured.update(url=url, json=json, timeout=timeout)
        return _ollama_ok()

    monkeypatch.setattr("app.main.requests.post", fake_post)
    client.post(URL, json=PAYLOAD)

    body = captured["json"]
    assert PAYLOAD["document_text"] in body["prompt"]
    assert PAYLOAD["question"] in body["prompt"]
    assert body["stream"] is False
    assert "num_ctx" in body["options"]


def test_respuesta_vacia_de_ollama(monkeypatch):
    monkeypatch.setattr("app.main.requests.post", lambda *a, **k: _ollama_ok("   "))
    r = client.post(URL, json=PAYLOAD)
    assert r.status_code == 200
    assert r.json()["answer"] == "Sin respuesta."


@pytest.mark.parametrize(
    "error, status",
    [
        (requests.exceptions.ConnectionError, 503),
        (requests.exceptions.Timeout, 504),
        (requests.exceptions.RequestException, 502),
    ],
)
def test_errores_de_red(monkeypatch, error, status):
    def boom(*args, **kwargs):
        raise error()

    monkeypatch.setattr("app.main.requests.post", boom)
    r = client.post(URL, json=PAYLOAD)
    assert r.status_code == status


def test_ollama_responde_con_error_http(monkeypatch):
    resp = MagicMock()
    resp.text = "model not found"
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError(response=resp)
    monkeypatch.setattr("app.main.requests.post", lambda *a, **k: resp)

    r = client.post(URL, json=PAYLOAD)
    assert r.status_code == 502
    assert "model not found" in r.json()["detail"]


def test_ollama_responde_json_invalido(monkeypatch):
    resp = MagicMock()
    resp.raise_for_status.return_value = None
    resp.json.side_effect = ValueError("no es JSON")
    monkeypatch.setattr("app.main.requests.post", lambda *a, **k: resp)

    r = client.post(URL, json=PAYLOAD)
    assert r.status_code == 502


@pytest.mark.parametrize(
    "payload",
    [
        {"document_text": "", "question": "x"},
        {"document_text": "x", "question": ""},
        {"question": "x"},
        {"document_text": "x"},
        {"document_text": "a" * (MAX_DOCUMENT_CHARS + 1), "question": "x"},
    ],
)
def test_validacion_de_entrada(payload):
    r = client.post(URL, json=payload)
    assert r.status_code == 422

def test_sin_api_key_devuelve_401():
    r = TestClient(app).post(URL, json=PAYLOAD)
    assert r.status_code == 401


def test_api_key_incorrecta_devuelve_403():
    r = TestClient(app, headers={"X-API-Key": "otra-clave"}).post(URL, json=PAYLOAD)
    assert r.status_code == 403


def test_health_no_requiere_api_key():
    assert TestClient(app).get("/health").status_code == 200
