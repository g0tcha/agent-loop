import pytest
from pydantic import ValidationError

from agent_loop.models.llm_response import LLMResponse
from agent_loop.models.tool_call import ToolCall
from agent_loop.models.usage import Usage


def _usage() -> Usage:
    return Usage(prompt_tokens=1, completion_tokens=2, total_tokens=3)


@pytest.mark.parametrize("finish_reason", ["stop", "tool_calls", "length"])
def test_llm_response_all_finish_reasons(finish_reason: str) -> None:
    r = LLMResponse(
        output_text="done",
        tool_calls=[],
        finish_reason=finish_reason,  # type: ignore[arg-type]
        usage=_usage(),
    )
    assert r.finish_reason == finish_reason


def test_llm_response_tool_calls_default_empty() -> None:
    r = LLMResponse(finish_reason="stop", usage=_usage())
    assert r.tool_calls == []


def test_llm_response_with_tool_calls() -> None:
    r = LLMResponse(
        output_text=None,
        tool_calls=[ToolCall(tool_name="t", tool_args={"a": 1})],
        finish_reason="tool_calls",
        usage=_usage(),
    )
    assert r.output_text is None
    assert len(r.tool_calls) == 1
    assert r.tool_calls[0].tool_name == "t"


def test_llm_response_invalid_finish_reason_rejected() -> None:
    with pytest.raises(ValidationError):
        LLMResponse(
            finish_reason="unknown",  # type: ignore[arg-type]
            usage=_usage(),
        )


def test_llm_response_nested_usage_validation() -> None:
    with pytest.raises(ValidationError):
        LLMResponse(
            finish_reason="stop",
            usage={"prompt_tokens": 1},  # type: ignore[arg-type]
        )


def test_llm_response_missing_finish_reason_rejected() -> None:
    with pytest.raises(ValidationError):
        LLMResponse.model_validate({"usage": _usage().model_dump()})
