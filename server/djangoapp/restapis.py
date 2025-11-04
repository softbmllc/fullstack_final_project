# server/djangoapp/restapis.py
import os
import requests

# Si tenés desplegado el microservicio Node con los endpoints
# /fetchDealer/<id>, /fetchReviews/dealer/<id>, /insert_review, etc.,
# definí aquí la URL base por variable de entorno en Code Engine:
#   DEALER_API = https://<tu-node-app>.appdomain.cloud
BASE_URL = os.environ.get("DEALER_API", "").rstrip("/")

def _make_url(path: str) -> str | None:
    """
    Devuelve la URL completa si BASE_URL está definido.
    Si path ya es una URL absoluta, la devuelve tal cual.
    Si no hay BASE_URL, devuelve None (modo stub).
    """
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if BASE_URL:
        if not path.startswith("/"):
            path = "/" + path
        return BASE_URL + path
    return None

def get_request(path: str) -> dict | list:
    """
    Hace GET al microservicio Node. Si no hay BASE_URL o falla la petición,
    devuelve {} / [] como stub para que las vistas no revienten.
    """
    url = _make_url(path)
    if not url:
        # Sin backend: permitir que las vistas sigan renderizando
        # (dealer_details mostrará datos en blanco, pero no tirará 500).
        return {}
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        # Puede ser lista o dict según el endpoint
        return resp.json()
    except Exception:
        return {}

def post_review(payload: dict) -> dict:
    """
    Hace POST al microservicio Node en /insert_review.
    Si no hay BASE_URL o falla la petición, devuelve un stub.
    """
    url = _make_url("/insert_review")
    if not url:
        return {"status": "stub", "detail": "No DEALER_API defined"}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"status": "error", "detail": str(e)}
