from dataclasses import dataclass
from typing import Literal

from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    RunContextWrapper,
    Runner,
    set_tracing_disabled,
)
from openai import AsyncAzureOpenAI
from openai.types.responses import EasyInputMessageParam

from spo_assistants.assistants.models import ChatMessage, ChatRole, SharePointContext
from spo_assistants.configuration.settings import Settings

# Don't export prompts/results to OpenAI's trace endpoint
# TODO: confirm if this is global or per module
set_tracing_disabled(True)

SITE_ASSISTANT_NAME = "Site Assistant"

# @dataclass gives you a plain data class with an auto-generated constructor. 
# Use it for internal data; 
# Pydantic models are for validating input from outside.
@dataclass
class AssistantExecutionContext:
    user_id: str
    share_point: SharePointContext

def _build_instructions(
        ctx: RunContextWrapper[AssistantExecutionContext],
        agent: Agent[AssistantExecutionContext],
) -> str:
    return "\n".join(
        [
            f"You are '{agent.name}', an AI assistant for the SharePoint Online site: "
            f"{ctx.context.share_point.site_url}",
            "",
            "Rules:",
            "- Be professional, concise, and direct.",
        ]
    )

def _to_input_item(message: ChatMessage) -> EasyInputMessageParam:
    # Literal["user", "assistant"] is a string-literal union type, like 'user' | 'assistant'.
    role: Literal["user", "assistant"] = "user" if message.role == ChatRole.USER else "assistant"
    return {"role": role, "content": message.content}

class SiteAssistantLlm:
    def __init__(self, settings: Settings) -> None:
        client = AsyncAzureOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key.get_secret_value(),
            api_version=settings.azure_openai_api_version
        )

        self._agent = Agent[AssistantExecutionContext](
            name = SITE_ASSISTANT_NAME,
            instructions=_build_instructions,
            model = OpenAIChatCompletionsModel(
                model=settings.azure_openai_deployment, 
                openai_client=client
            ),
            model_settings=ModelSettings(max_tokens=settings.azure_openai_max_output_tokens)
        )

    async def execute(
        self, 
        context: AssistantExecutionContext,
        messages: list[ChatMessage]
    ) -> str:
        result = await Runner.run(
            self._agent,
            [_to_input_item(m) for m in messages],
            context=context, 
            max_turns=10
        )

        return str(result.final_output or "")