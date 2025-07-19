"""Basic event loop for outbound calls."""
import time

from app.modules.asr_whisper import WhisperASR
from app.modules.llm_ollama import OllamaLLM
from app.modules.tts_piper import PiperTTS
from app.modules.scheduler import CallScheduler
from app.modules.dialer import OutboundDialer
from app.core.call_handler import CallHandler
from app.core.context_manager import ContextManager


def main() -> None:
    scheduler = CallScheduler()
    dialer = OutboundDialer()
    handler = CallHandler(WhisperASR(), OllamaLLM(), PiperTTS(), ContextManager())

    while True:
        if scheduler.should_call_now():
            extension = dialer.dial()
            audio = handler.handle("/tmp/input.wav")
            print(f"[CALL {extension}] Generated {len(audio)} bytes")
        time.sleep(1)


if __name__ == "__main__":
    main()
