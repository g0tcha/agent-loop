import pytest
from pydantic import ValidationError

from agent_loop.models.tool_definition import ToolDefinition


def test_tool_definition_valid() -> None:
    td = ToolDefinition(
        name="get_weather",
        description="Returns weather for a city.",
        parameters={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    )
    assert td.name == "get_weather"
    assert "city" in td.parameters.get("properties", {})


def test_tool_definition_missing_field_rejected() -> None:
    with pytest.raises(ValidationError):
        ToolDefinition.model_validate(
            {"name": "x", "description": "y"},
        )


def test_tool_definition_parameters_must_be_dict() -> None:
    with pytest.raises(ValidationError):
        ToolDefinition(name="x", description="y", parameters="bad")  # type: ignore[arg-type]
