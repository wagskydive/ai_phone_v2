class BaseASR:
    """Base interface for ASR modules."""

    def transcribe(self, audio_path: str) -> str:
        """Transcribe an audio file to text."""
        raise NotImplementedError
