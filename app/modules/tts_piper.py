from app.modules.tts import BaseTTS


class PiperTTS(BaseTTS):
    """Placeholder TTS module using Piper."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path
        # In real implementation a Piper voice would be loaded here

    def synthesize(self, text: str) -> bytes:
        """Return dummy audio bytes."""
        # TODO: integrate with Piper TTS
        return b"audio-bytes"
