from pydantic import BaseModel, Field
from typing import Literal
from agent_loop.models.tool_call import ToolCall
from agent_loop.models.usage import Usage

class LLMResponse(BaseModel):
    output_text: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    finish_reason: Literal["stop", "tool_calls", "length"]
    usage: Usage
