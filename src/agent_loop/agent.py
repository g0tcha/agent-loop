import json
from typing import Protocol

from agent_loop.models.llm_request import LLMRequest
from agent_loop.models.llm_response import LLMResponse
from agent_loop.models.message import Message
from agent_loop.tools.tool_registry import ToolRegistry


class LLMClient(Protocol):
    def call(self, request: LLMRequest) -> LLMResponse: ...


class Agent:
    def __init__(self, tool_registry: ToolRegistry, llm_client: LLMClient) -> None:
        self._tool_registry = tool_registry
        self._llm_client = llm_client

    def run(self, message: str) -> LLMResponse:
        messages: list[Message] = [Message(role="user", content=message)]
        tools = self._tool_registry.definitions()

        while True:
            response = self._llm_client.call(
                LLMRequest(messages=messages, tools=tools),
            )

            if response.finish_reason != "tool_calls" or not response.tool_calls:
                return response

            messages.append(
                Message(
                    role="assistant",
                    content=response.output_text or "",
                    tool_calls=response.tool_calls,
                )
            )

            for tool_call in response.tool_calls:
                tool = self._tool_registry.get(tool_call.tool_name)
                if tool is None:
                    result: dict[str, object] = {
                        "error": f"Unknown tool: {tool_call.tool_name}",
                    }
                else:
                    result = tool.execute(tool_call.tool_args)

                messages.append(
                    Message(
                        role="tool",
                        content=json.dumps(result),
                        tool_call_id=tool_call.id,
                    )
                )
