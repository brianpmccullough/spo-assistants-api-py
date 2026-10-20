from fastapi.testclient import TestClient

from spo_assistants.assistants.dependencies import get_site_assistant_service
from spo_assistants.assistants.integrity import ChatIntegrityService
from spo_assistants.assistants.service import SiteAssistantService
from spo_assistants.main import app

client = TestClient(app)
# Avoid loading Settings (needs .env / real secrets) in tests;
# this just hardcodes the secret "test-secret"
app.dependency_overrides[get_site_assistant_service] = lambda: SiteAssistantService(
    ChatIntegrityService("test-secret")
)


def test_site_assistant_configuration_uses_camel_case() -> None:
    response = client.get("/assistants/site-assistant")
    assert response.status_code == 200
    assert response.json()["assistantId"] == "site-assistant"


def test_chat_round_trip() -> None:
    body = {"message": "hello", "context": {"siteUrl": "https://contoso.sharepoint.com/sites/x"}}
    first = client.post("/assistants/site-assistant/chat", json=body)
    assert first.status_code == 200

    second = client.post(
        "/assistants/site-assistant/chat",
        json={**body, "message": "again", "state": first.json()["state"]},
    )
    assert second.status_code == 200
    assert len(second.json()["state"]["history"]) == 4
