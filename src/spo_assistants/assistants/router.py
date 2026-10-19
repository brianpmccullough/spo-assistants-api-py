from fastapi import APIRouter

from spo_assistants.assistants.models import AssistantConfiguration

router = APIRouter(prefix="/assistants/site-assistant", tags=["site-assistant"])

@router.get("")
def get_configuration() -> AssistantConfiguration:
    return AssistantConfiguration(
        assistant_id="site-assistant",
        greeting="Ask me about this site...",
        starter_prompts=[]
    )