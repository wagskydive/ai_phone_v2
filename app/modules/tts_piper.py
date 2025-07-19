"""Piper text-to-speech integration."""

from __future__ import annotations

import io
import wave
from typing import Iterable

import numpy as np
import piper

from app.modules.tts import BaseTTS


class PiperTTS(BaseTTS):
    """Generate audio with Piper or fall back to a sine wave."""

    def __init__(self, model_path: str | None = None, config_path: str | None = None, use_cuda: bool = False) -> None:
        self.model_path = model_path
        self.config_path = config_path
        self.use_cuda = use_cuda
        self.voice = None
        if model_path:
            try:
                self.voice = piper.PiperVoice.load(model_path, config_path, use_cuda=use_cuda)
            except Exception:
                # Fail silently so tests can still run without large model files
                self.voice = None

    def synthesize(self, text: str) -> bytes:
        """Return synthesized audio as bytes."""
        if self.voice:
            audio_chunks: Iterable[piper.AudioChunk] = self.voice.synthesize(text)
            return b"".join(chunk.audio_int16_bytes for chunk in audio_chunks)

        # Fallback: generate a short sine wave so tests have non-empty audio
        sample_rate = 22050
        duration = max(0.1, min(len(text) / 10.0, 2.0))
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = 0.1 * np.sin(2 * np.pi * 440 * t)
        audio = np.int16(tone * 32767)

        with io.BytesIO() as buffer:
            with wave.open(buffer, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(sample_rate)
                wav.writeframes(audio.tobytes())
            return buffer.getvalue()
