from typing import Any

from agent_loop.models.tool_definition import ToolDefinition
from agent_loop.tools.base import Tool


class BTCPriceTool(Tool):
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_btc_price",
            description="Returns the current BTC price in USD.",
            parameters={
                "type": "object",
                "properties": {},
            },
        )

    def execute(self, args: dict[str, Any]) -> dict[str, Any]:
        return {"price": 75000}
