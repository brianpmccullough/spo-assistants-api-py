import pytest
from fastapi import HTTPException

from spo_assistants.assistants.integrity import ChatIntegrityService
from spo_assistants.assistants.models import ChatRequest, SharePointContext
from spo_assistants.assistants.service import SiteAssistantService

integrity = ChatIntegrityService("test-secret")
service = SiteAssistantService(integrity)
context = SharePointContext(site_url="https://contoso.sharepoint.com/sites/x")


def test_first_message_returns_signed_state() -> None:
    response = service.chat("user-1", ChatRequest(message="hi", context=context))
    assert len(response.state.history) == 2
    assert integrity.verify("user-1", response.state.history, response.state.signature)


def test_tampered_history_is_rejected() -> None:
    first = service.chat("user-1", ChatRequest(message="hi", context=context))
    first.state.history[0].content = "tampered"
    with pytest.raises(HTTPException):
        service.chat("user-1", ChatRequest(message="next", context=context, state=first.state))
