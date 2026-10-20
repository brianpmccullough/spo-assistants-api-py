import time
from uuid import uuid4

from fastapi import HTTPException

from spo_assistants.assistants.integrity import ChatIntegrityService
from spo_assistants.assistants.models import (
    MAX_HISTORY_LENGTH,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ChatRole,
    ChatState,
)


def _now_ms() -> float:
    return time.time() * 1000  # matches JS Date.now()


def _trim(messages: list[ChatMessage]) -> list[ChatMessage]:
    # [-50:] syntax below is equivalent of slice()
    return messages[-MAX_HISTORY_LENGTH:]


class SiteAssistantService:
    def __init__(self, integrity: ChatIntegrityService) -> None:
        self._integrity = integrity

    def chat(self, user_id: str, request: ChatRequest) -> ChatResponse:
        state = request.state
        if state and not self._integrity.verify(user_id, state.history, state.signature):
            raise HTTPException(status_code=400, detail="Invalid chat state")

        chat_id = state.chat_id if state else uuid4()
        prior = state.history if state else []

        messages = _trim(
            [*prior, ChatMessage(role=ChatRole.USER, content=request.message, timestamp=_now_ms())]
        )
        reply = f"you said... {request.message}"  # stub; LLM replaces this

        history = _trim(
            [*messages, ChatMessage(role=ChatRole.ASSISTANT, content=reply, timestamp=_now_ms())]
        )
        return ChatResponse(
            message=reply,
            state=ChatState(
                chat_id=chat_id, history=history, signature=self._integrity.sign(user_id, history)
            ),
        )
