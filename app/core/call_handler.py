from app.core.context_manager import ContextManager


class CallHandler:
    """Manage a single call by orchestrating ASR, LLM, and TTS."""

    def __init__(self, asr, llm, tts, context: ContextManager | None = None):
        self.asr = asr
        self.llm = llm
        self.tts = tts
        self.context = context or ContextManager()

    def handle(self, audio_path: str) -> bytes:
        """Process an audio file and return audio response."""
        text = self.asr.transcribe(audio_path)
        self.context.add_entry(text)
        reply = self.llm.generate(self.context.summarize())
        self.context.add_entry(reply)
        audio = self.tts.synthesize(reply)
        return audio

