import json
from typing import Any

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from agent_loop.core.http.exception import (
    HTTPAuthenticationError,
    HTTPInvalidResponseError,
    HTTPRateLimitError,
    HTTPTransportError,
)


class HTTPTransport:

    def post_json(
        self,
        url: str,
        headers: dict[str, str],
        body: bytes,
        *,
        timeout: float = 120,
    ) -> dict[str, Any]:
        req = Request(url, data=body, method="POST", headers=headers)
        try:
            with urlopen(req, timeout=timeout) as resp:
                try:
                    raw = resp.read().decode("utf-8")
                except UnicodeDecodeError as e:
                    raise HTTPInvalidResponseError(
                        "Corps de réponse HTTP illisible en UTF-8.",
                    ) from e
        except HTTPError as e:
            detail = self._http_error_detail(e)
            if e.code == 401:
                raise HTTPAuthenticationError(detail) from e
            if e.code == 429:
                raise HTTPRateLimitError(detail) from e
            raise HTTPTransportError(detail) from e
        except URLError as e:
            raise HTTPTransportError(str(e.reason or e)) from e
        except TimeoutError as e:
            raise HTTPTransportError("Dépassement du délai d'attente HTTP.") from e

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as e:
            raise HTTPInvalidResponseError("Réponse HTTP non JSON.") from e

        if not isinstance(parsed, dict):
            raise HTTPInvalidResponseError(
                "Réponse JSON attendue sous forme d'objet à la racine.",
            )

        return parsed

    @staticmethod
    def _http_error_detail(exc: HTTPError) -> str:
        try:
            body = exc.read().decode("utf-8")
        except OSError:
            body = ""
        prefix = f"HTTP {exc.code}"
        return f"{prefix}: {body}" if body else prefix
