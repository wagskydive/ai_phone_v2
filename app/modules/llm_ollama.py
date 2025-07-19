from app.modules.llm import BaseLLM


class OllamaLLM(BaseLLM):
    """Placeholder LLM module using an Ollama API."""

    def __init__(self, endpoint: str = "http://localhost:11434") -> None:
        self.endpoint = endpoint
        # Real implementation would set up HTTP client here

    def generate(self, prompt: str) -> str:
        """Return a canned response for now."""
        # TODO: integrate with actual Ollama server
        return f"You said: {prompt}"
