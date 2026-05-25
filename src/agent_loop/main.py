from agent_loop.models.llm_request import LLMRequest
from agent_loop.llm.providers.openai.client import OpenAIClient
from agent_loop.models.message import Message


def main() -> None:
    r = OpenAIClient().call(
        LLMRequest(
            messages=[Message(role="user", content="Salut. Je test simplement l'API.")],
            tools=[],
        ),
    )
    print(r.model_dump())


if __name__ == "__main__":
    main()
