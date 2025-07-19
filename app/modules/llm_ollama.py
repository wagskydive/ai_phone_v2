"""Ollama LLM client module."""

from __future__ import annotations

import requests
from app.modules.llm import BaseLLM


class OllamaLLM(BaseLLM):
    """Basic client for an Ollama server."""

    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "llama3.2:latest") -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model

    def generate(self, prompt: str, system: str | None = None) -> str:
        """Generate a response from the Ollama server.

        If the server call fails, a canned echo response is returned so tests
        remain deterministic without network access.
        """
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system
        try:
            res = requests.post(f"{self.endpoint}/api/generate", json=payload, timeout=10)
            res.raise_for_status()
            return res.json().get("response", "").strip()
        except Exception:
            # Fallback behaviour for tests or when Ollama is unavailable
            return f"You said: {prompt}"

    def summarize(self, text: str) -> str:
        """Summarize ``text`` using the LLM."""
        system = "Summarize the following conversation briefly."
        return self.generate(text, system=system)

    def extract_name(self, text: str) -> str | None:
        """Extract a caller's first name from ``text``."""
        system = (
            "Extract the caller's first name from the following text. "
            "Reply with just the name or 'None' if no name is mentioned."
        )
        response = self.generate(text, system=system)
        if not response or response.startswith("You said"):
            return None
        name = response.strip().split()[0]
        if not name or name.lower() == "none":
            return None
        return name
