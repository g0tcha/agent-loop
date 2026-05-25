from pydantic import BaseModel
from agent_loop.models.message import Message
from agent_loop.models.tool_definition import ToolDefinition


class LLMRequest(BaseModel):
    messages: list[Message]
    tools: list[ToolDefinition]
    max_tokens: int | None = None
