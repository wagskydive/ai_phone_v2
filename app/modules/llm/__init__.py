class BaseLLM:
    """Base interface for LLM modules."""

    def generate(self, prompt: str) -> str:
        """Generate a text response from a prompt."""
        raise NotImplementedError
