from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_flujo_completo():
    # Chat
    mensaje = {"contenido": "Hola, quiero una laptop de gaming"}
    r_chat = client.post("/api/chat", json=mensaje)
    assert r_chat.status_code == 200
    assert len(r_chat.json()["respuesta"]) > 0

    # Feedback
    feedback = {"id_venta": "1000", "puntuacion": 5, "recomendacion": 1, "comentario": "Excelente atención"}
    r_feedback = client.post("/api/feedback", json=feedback)
    assert r_feedback.status_code == 200
    assert r_feedback.json()["status"] == "ok"