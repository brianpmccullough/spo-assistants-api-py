from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from spo_assistants.assistants.integrity import ChatIntegrityService
from spo_assistants.assistants.service import SiteAssistantService
from spo_assistants.configuration.settings import get_settings


@lru_cache
def get_integrity_service() -> ChatIntegrityService:
    secret = get_settings().chat_hmac_secret.get_secret_value()
    return ChatIntegrityService(secret)


IntegrityServiceDep = Annotated[ChatIntegrityService, Depends(get_integrity_service)]

@lru_cache
def get_site_assistant_service() -> SiteAssistantService:
    return SiteAssistantService(get_integrity_service())

SiteAssistantServiceDep = Annotated[SiteAssistantService, Depends(get_site_assistant_service)]

def get_current_user_id() -> str:
    return "local-dev-user" # TODO: replace this with bearer token user

CurrentUserIdDep = Annotated[str, Depends(get_current_user_id)]