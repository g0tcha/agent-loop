from pydantic import BaseModel
from .message import Message
from .tool_definition import ToolDefinition


class LLMRequest(BaseModel):
    messages: list[Message]
    tools: list[ToolDefinition]
    max_tokens: int | None = None
