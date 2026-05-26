from pydantic import BaseModel
from typing import Any

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]