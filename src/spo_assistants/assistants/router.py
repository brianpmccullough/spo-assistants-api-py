from fastapi import APIRouter

from spo_assistants.assistants.dependencies import CurrentUserIdDep, SiteAssistantServiceDep
from spo_assistants.assistants.models import AssistantConfiguration, ChatRequest, ChatResponse

router = APIRouter(prefix="/assistants/site-assistant", tags=["site-assistant"])

@router.get("")
def get_configuration() -> AssistantConfiguration:
    return AssistantConfiguration(
        assistant_id="site-assistant",
        greeting="Ask me about this site...",
        starter_prompts=[]
    )

@router.post("/chat")
def chat(
    request: ChatRequest,
    user_id: CurrentUserIdDep,
    service: SiteAssistantServiceDep,
) -> ChatResponse:
    return service.chat(user_id, request)