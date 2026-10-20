from spo_assistants.assistants.integrity import ChatIntegrityService
from spo_assistants.assistants.models import ChatMessage, ChatRole

service = ChatIntegrityService("test-secret")
history = [ChatMessage(role=ChatRole.USER, content="hi", timestamp=0)]


def test_verify_accepts_own_signature() -> None:
    signature = service.sign("user-1", history)
    assert service.verify("user-1", history, signature)


def test_verify_rejects_different_user() -> None:
    signature = service.sign("user-1", history)
    assert not service.verify("user-2", history, signature)


def test_verify_rejects_malformed_signature() -> None:
    assert not service.verify("user-1", history, "short")
