from app.core.context_manager import ContextManager


class CallHandler:
    """Manage a single call by orchestrating ASR, LLM, and TTS."""

    def __init__(self, asr, llm, tts, context: ContextManager | None = None,
                 storage_path: str | None = None):
        """Create a call handler.

        Parameters
        ----------
        asr, llm, tts
            Module instances used during the call.
        context
            Optional pre-configured context manager instance.
        storage_path
            Path to a memory file for persistent history if ``context`` is not
            provided.
        """
        self.asr = asr
        self.llm = llm
        self.tts = tts
        # Use provided context or create one, optionally with persistence
        self.context = context or ContextManager(storage_path=storage_path)

    def handle(self, audio_path: str) -> bytes:
        """Process an audio file and return audio response."""
        text = self.asr.transcribe(audio_path)
        self.context.add_entry(text)
        reply = self.llm.generate(self.context.summarize())
        self.context.add_entry(reply)
        audio = self.tts.synthesize(reply)
        return audio

