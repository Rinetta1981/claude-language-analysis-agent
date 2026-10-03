from typing import Protocol

class LanguageModelProvider(Protocol):
    def analyze(self, request: str, text: str) -> dict:
        ...
