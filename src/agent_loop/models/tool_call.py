from pydantic import BaseModel
from typing import Any

class ToolCall(BaseModel):
    id: str
    tool_name: str
    tool_args: dict[str, Any]