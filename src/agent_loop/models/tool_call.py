from pydantic import BaseModel

class ToolCall(BaseModel):
    tool_name: str
    tool_args: dict