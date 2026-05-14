import pytest
from pydantic import ValidationError

from agent_loop.models.tool_call import ToolCall


def test_tool_call_valid() -> None:
    tc = ToolCall(tool_name="search", tool_args={"q": "cats", "limit": 5})
    assert tc.tool_name == "search"
    assert tc.tool_args == {"q": "cats", "limit": 5}


def test_tool_call_empty_args_dict() -> None:
    tc = ToolCall(tool_name="noop", tool_args={})
    assert tc.tool_args == {}


def test_tool_call_missing_fields_rejected() -> None:
    with pytest.raises(ValidationError):
        ToolCall.model_validate({"tool_name": "x"})
    with pytest.raises(ValidationError):
        ToolCall.model_validate({"tool_args": {}})


def test_tool_call_tool_args_must_be_dict() -> None:
    with pytest.raises(ValidationError):
        ToolCall(tool_name="x", tool_args="not-a-dict")  # type: ignore[arg-type]
