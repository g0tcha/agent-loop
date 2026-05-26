from pydantic import BaseModel
from typing import Literal

from agent_loop.models.tool_call import ToolCall


class Message(BaseModel):
    role: Literal["user", "assistant", "system", "tool"]
    content: str
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None