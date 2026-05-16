from urllib.request import Request, urlopen


class HTTPTransport:

    def post(self, url: str, headers: dict[str, str], body: bytes, *, timeout: float = 120) -> bytes:
        req = Request(url, data=body, method="POST", headers=headers)
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
