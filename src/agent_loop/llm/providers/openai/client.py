import json

from agent_loop.config import settings
from agent_loop.llm.models.llm_request import LLMRequest
from agent_loop.llm.models.llm_response import LLMResponse
from agent_loop.llm.providers.openai.mapper import OpenAIMapper
from agent_loop.llm.providers.openai.transport import HTTPTransport

_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIClient:
    def __init__(
        self,
        transport: HTTPTransport | None = None,
        mapper: OpenAIMapper | None = None,
    ) -> None:
        self._transport = transport or HTTPTransport()
        self._mapper = mapper or OpenAIMapper()

    def call(self, request: LLMRequest) -> LLMResponse:
        payload = self._mapper.request_to_payload(request, settings.default_model)
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        raw = self._transport.post(_CHAT_COMPLETIONS_URL, headers, body)
        data = json.loads(raw.decode("utf-8"))
        return self._mapper.response_body_to_llm_response(data)
