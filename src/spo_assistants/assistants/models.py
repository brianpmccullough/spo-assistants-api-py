from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

MAX_MESSAGE_LENGTH = 4000
MAX_HISTORY_LENGTH = 50

class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class AssistantConfiguration(ApiModel):
    assistant_id: str
    greeting: str
    starter_prompts: list[str]

class ChatRole(StrEnum):
    USER = "user"
    ROLE = "role"

class ChatMessage(ApiModel):
    role: ChatRole
    content: str
    timestamp: float

class ChatState(ApiModel):
    chat_id: UUID
    history: Annotated[list[ChatMessage], Field(max_length=MAX_HISTORY_LENGTH)]
    signature: str

class SharePointContext(ApiModel):
    site_url: Annotated[str, Field(min_length=1)]
    page_url: str | None = None

class ChatRequest(ApiModel):
    message: Annotated[str, Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)]
    context: SharePointContext
    state: ChatState | None = None

class ChatResponse(ApiModel):
    message: str
    state: ChatState

