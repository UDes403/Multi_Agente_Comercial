from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_responde():
    payload = {"contenido": "Hola, quiero ver laptops para gaming"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    assert "respuesta" in response.json()