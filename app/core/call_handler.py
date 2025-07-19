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
        self.context = context or ContextManager(storage_path=storage_path, llm=self.llm)

    def handle(self, audio_path: str, interrupt_fn=None) -> bytes:
        """Process an audio file and return audio response.

        Parameters
        ----------
        audio_path
            Path to the recorded caller audio.
        interrupt_fn
            Optional callable returning ``True`` if playback should stop.
        """
        text = self.asr.transcribe(audio_path)
        self.context.add_entry(text)
        prompt = self.context.get_context()
        reply = self.llm.generate(prompt)
        if self.context.caller_name:
            reply = f"Hello {self.context.caller_name}, " + reply
        self.last_reply = reply
        self.context.add_entry(reply)
        audio = self.tts.synthesize(reply)
        # persist summary so next call includes this dialogue
        self.context.save_summary()
        if interrupt_fn and interrupt_fn():
            # playback interrupted before completion
            return b""
        return audio

