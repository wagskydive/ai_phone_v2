class CallHandler:
    """Manage a single call by orchestrating ASR, LLM, and TTS."""

    def __init__(self, asr, llm, tts):
        self.asr = asr
        self.llm = llm
        self.tts = tts

    def handle(self, audio_path: str) -> bytes:
        """Process an audio file and return audio response."""
        text = self.asr.transcribe(audio_path)
        reply = self.llm.generate(text)
        audio = self.tts.synthesize(reply)
        return audio

