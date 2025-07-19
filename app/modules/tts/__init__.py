class BaseTTS:
    """Base interface for TTS modules."""

    def synthesize(self, text: str) -> bytes:
        """Convert text to speech and return audio bytes."""
        raise NotImplementedError
