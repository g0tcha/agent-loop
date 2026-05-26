import json
from typing import Any, Literal

from agent_loop.models.llm_request import LLMRequest
from agent_loop.models.llm_response import LLMResponse
from agent_loop.llm.providers.openai.exception import OpenAIInvalidResponseError
from agent_loop.models.tool_call import ToolCall
from agent_loop.models.usage import Usage

_FINISH_REASONS = frozenset({"stop", "tool_calls", "length"})


class OpenAIMapper:
    """Construction du corps de requête et lecture de la réponse OpenAI."""

    def messages_payload(self, request: LLMRequest) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for m in request.messages:
            if m.role == "assistant" and m.tool_calls:
                out.append(
                    {
                        "role": "assistant",
                        "content": m.content or None,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.tool_name,
                                    "arguments": json.dumps(tc.tool_args),
                                },
                            }
                            for tc in m.tool_calls
                        ],
                    }
                )
            elif m.role == "tool":
                out.append(
                    {
                        "role": "tool",
                        "content": m.content,
                        "tool_call_id": m.tool_call_id,
                    }
                )
            else:
                out.append({"role": m.role, "content": m.content})
        return out

    def tools_payload(self, request: LLMRequest) -> list[dict[str, Any]] | None:
        if not request.tools:
            return None
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
            }
            for t in request.tools
        ]

    def map_finish_reason(self, raw: str | None) -> Literal["stop", "tool_calls", "length"]:
        if raw in _FINISH_REASONS:
            return raw  # type: ignore[return-value]
        return "stop"

    def parse_tool_calls(self, message: dict[str, Any]) -> list[ToolCall]:
        out: list[ToolCall] = []
        for tc in message.get("tool_calls") or []:
            fn = tc.get("function") or {}
            name = str(fn.get("name", ""))
            raw_args = fn.get("arguments") or "{}"
            if isinstance(raw_args, str):
                try:
                    args: dict[str, Any] = json.loads(raw_args)
                except json.JSONDecodeError:
                    args = {}
            elif isinstance(raw_args, dict):
                args = raw_args
            else:
                args = {}
            out.append(
                ToolCall(
                    id=str(tc.get("id", "")),
                    tool_name=name,
                    tool_args=args,
                )
            )
        return out

    def request_to_payload(self, request: LLMRequest, model: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "messages": self.messages_payload(request),
        }
        tools = self.tools_payload(request)
        if tools is not None:
            payload["tools"] = tools
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens
        return payload

    def response_body_to_llm_response(self, data: dict[str, Any]) -> LLMResponse:
        choices = data.get("choices") or []
        if not choices:
            msg = "Réponse OpenAI sans choix (choices vides)."
            raise OpenAIInvalidResponseError(msg)

        choice0 = choices[0]
        message = choice0.get("message") or {}
        finish_reason = self.map_finish_reason(choice0.get("finish_reason"))

        content = message.get("content")
        output_text = content if isinstance(content, str) else None
        tool_calls = self.parse_tool_calls(message)

        usage_raw = data.get("usage") or {}
        usage = Usage(
            prompt_tokens=int(usage_raw.get("prompt_tokens", 0)),
            completion_tokens=int(usage_raw.get("completion_tokens", 0)),
            total_tokens=int(usage_raw.get("total_tokens", 0)),
        )

        return LLMResponse(
            output_text=output_text,
            tool_calls=tool_calls,
            finish_reason=finish_reason,
            usage=usage,
        )
