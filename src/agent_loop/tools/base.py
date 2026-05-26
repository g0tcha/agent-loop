from abc import ABC, abstractmethod
from typing import Any

from agent_loop.models.tool_definition import ToolDefinition


class Tool(ABC):
    @abstractmethod
    def definition(self) -> ToolDefinition:
        pass

    @abstractmethod
    def execute(self, args: dict[str, Any]) -> dict[str, Any]:
        pass
