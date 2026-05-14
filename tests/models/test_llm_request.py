import pytest
from pydantic import ValidationError

from agent_loop.models.llm_request import LLMRequest
from agent_loop.models.message import Message
from agent_loop.models.tool_definition import ToolDefinition


def _sample_messages() -> list[Message]:
    return [
        Message(role="system", content="You are helpful."),
        Message(role="user", content="Hi"),
    ]


def _sample_tools() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="echo",
            description="Echo input",
            parameters={"type": "object", "properties": {}},
        ),
    ]


def test_llm_request_valid_with_max_tokens() -> None:
    q = LLMRequest(
        messages=_sample_messages(),
        tools=_sample_tools(),
        max_tokens=256,
    )
    assert len(q.messages) == 2
    assert len(q.tools) == 1
    assert q.max_tokens == 256


def test_llm_request_max_tokens_optional_default_none() -> None:
    q = LLMRequest(messages=_sample_messages(), tools=_sample_tools())
    assert q.max_tokens is None


def test_llm_request_nested_message_validation() -> None:
    with pytest.raises(ValidationError):
        LLMRequest(
            messages=[{"role": "invalid", "content": "ok"}],  # type: ignore[list-item]
            tools=_sample_tools(),
        )


def test_llm_request_nested_tool_validation() -> None:
    with pytest.raises(ValidationError):
        LLMRequest(
            messages=_sample_messages(),
            tools=[{"name": "only_name"}],  # type: ignore[list-item]
        )


def test_llm_request_missing_messages_rejected() -> None:
    with pytest.raises(ValidationError):
        LLMRequest.model_validate({"tools": _sample_tools()})
