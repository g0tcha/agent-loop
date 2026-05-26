from agent_loop.models.tool_definition import ToolDefinition
from agent_loop.tools.base import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        definition = tool.definition()
        self._tools[definition.name] = tool

    def definitions(self) -> list[ToolDefinition]:
        return [tool.definition() for tool in self._tools.values()]

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)
