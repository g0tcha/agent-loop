from pydantic import BaseModel, Field
from typing import Literal
from .tool_call import ToolCall
from .usage import Usage

class LLMResponse(BaseModel):
    output_text: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    finish_reason: Literal["stop", "tool_calls", "length"]
    usage: Usage