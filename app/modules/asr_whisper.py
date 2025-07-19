"""Whisper-based speech-to-text module."""

from app.modules.asr import BaseASR
import whisper


class WhisperASR(BaseASR):
    """Placeholder ASR module using Whisper."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path or "base"
        # Load Whisper model once during initialization
        self.model = whisper.load_model(self.model_path)

    def transcribe(self, audio_path: str) -> str:
        """Transcribe the given audio file using Whisper."""
        result = self.model.transcribe(audio_path, fp16=False)
        return result.get("text", "").strip()
