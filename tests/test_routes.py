from fastapi.testclient import TestClient

from spo_assistants.main import app

client = TestClient(app)

def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_site_assistant_configuration_uses_camel_case() -> None:
    response = client.get("/assistants/site-assistant")
    assert response.status_code == 200
    assert response.json()["assistantId"] == "site-assistant"
    