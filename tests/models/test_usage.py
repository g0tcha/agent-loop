import pytest
from pydantic import ValidationError

from agent_loop.models.usage import Usage


def test_usage_valid() -> None:
    u = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    assert u.prompt_tokens == 10
    assert u.completion_tokens == 20
    assert u.total_tokens == 30


@pytest.mark.parametrize(
    "field",
    ["prompt_tokens", "completion_tokens", "total_tokens"],
)
def test_usage_missing_field_rejected(field: str) -> None:
    data = {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3}
    del data[field]
    with pytest.raises(ValidationError):
        Usage.model_validate(data)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"prompt_tokens": "x", "completion_tokens": 0, "total_tokens": 0},
        {"prompt_tokens": 0, "completion_tokens": [], "total_tokens": 0},
        {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 1.5},
    ],
)
def test_usage_invalid_types(kwargs: dict) -> None:
    with pytest.raises(ValidationError):
        Usage(**kwargs)
