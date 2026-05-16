"""Exceptions levées pour des réponses OpenAI hors contrat attendu."""


class OpenAIInvalidResponseError(Exception):
    """Réponse Chat Completions incompatible avec le schéma attendu (ex. liste choices vide ou absente)."""
