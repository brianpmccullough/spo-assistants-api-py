from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class AssistantConfiguration(ApiModel):
    assistant_id: str
    greeting: str
    starter_prompts: list[str]
