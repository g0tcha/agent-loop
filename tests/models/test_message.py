import pytest
from pydantic import ValidationError

from agent_loop.models.message import Message


@pytest.mark.parametrize("role", ["user", "assistant", "system", "tool"])
def test_message_valid_roles(role: str) -> None:
    m = Message(role=role, content="hello")
    assert m.role == role
    assert m.content == "hello"


def test_message_invalid_role_rejected() -> None:
    with pytest.raises(ValidationError):
        Message(role="admin", content="x")  # type: ignore[arg-type]


def test_message_missing_content_rejected() -> None:
    with pytest.raises(ValidationError):
        Message.model_validate({"role": "user"})


def test_message_content_not_string_rejected() -> None:
    with pytest.raises(ValidationError):
        Message(role="user", content=123)  # type: ignore[arg-type]
