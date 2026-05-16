"""Exceptions HTTP génériques (couche core)."""


class HTTPTransportError(Exception):
    """Erreur réseau, timeout, ou réponse HTTP non gérée par une classe dédiée (ex. 5xx)."""


class HTTPAuthenticationError(Exception):
    """Réponse HTTP 401 — authentification refusée."""


class HTTPRateLimitError(Exception):
    """Réponse HTTP 429 — limite de débit ou quota dépassé."""


class HTTPInvalidResponseError(Exception):
    """Corps de réponse illisible en UTF-8 ou JSON invalide / non objet à la racine."""
