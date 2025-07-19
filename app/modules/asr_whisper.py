from app.modules.asr import BaseASR


class WhisperASR(BaseASR):
    """Placeholder ASR module using Whisper."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path
        # In real implementation a Whisper model would be loaded here

    def transcribe(self, audio_path: str) -> str:
        """Return dummy transcription for given audio."""
        # TODO: integrate with Whisper ASR
        return "Hello"
