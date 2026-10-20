import pytest
from pydantic import ValidationError

from spo_assistants.assistants.models import MAX_HISTORY_LENGTH, ChatRequest

TEST_URL = "https://contoso.sharepoint.com/sites/foo"

def test_parses_camel_case_json() -> None:
    request = ChatRequest.model_validate(
        {"message": "hi", "context": {"siteUrl": TEST_URL}}
    )
    assert request.context.site_url == TEST_URL
    assert request.state is None

def test_rejects_empty_message() -> None:
    with pytest.raises(ValidationError):
        ChatRequest.model_validate({"message": "", "context": {"siteUrl": "x"}})

def test_rejects_history_over_max() -> None:
    message = {"role": "user", "content": "hi", "timestamp": 0}
    with pytest.raises(ValidationError):
        ChatRequest.model_validate(
            {
                "message": "hi",
                "context": {"siteUrl": "x"},
                "state": {
                    "chatId": "00000000-0000-0000-0000-000000000000",
                    "history": [message] * (MAX_HISTORY_LENGTH + 1),
                    "signature": "sig",
                },
            }
        )