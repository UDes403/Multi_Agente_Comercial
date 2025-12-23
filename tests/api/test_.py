from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_feedback_registra():
    payload = {"id_venta": "999", "puntuacion": 5, "recomendacion": 1, "comentario": "Muy buena experiencia"}
    response = client.post("/api/feedback", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
