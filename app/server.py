"""Minimal HTTP interface for call processing."""
from __future__ import annotations

import io
import os
import tempfile

from flask import Flask, request, send_file, jsonify

from app.modules.asr_whisper import WhisperASR
from app.modules.llm_ollama import OllamaLLM
from app.modules.tts_piper import PiperTTS
from app.core.call_handler import CallHandler
from app.core.context_manager import ContextManager

app = Flask(__name__)

asr = WhisperASR()
llm = OllamaLLM()
tts = PiperTTS()
handler = CallHandler(asr, llm, tts, ContextManager())

@app.route('/process', methods=['POST'])
def process():
    """Process uploaded audio and return synthesized speech."""
    uploaded = request.files.get('audio')
    if not uploaded:
        return jsonify({'error': 'no audio provided'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        uploaded.save(tmp.name)
        audio_bytes = handler.handle(tmp.name)
    os.unlink(tmp.name)

    return send_file(io.BytesIO(audio_bytes), mimetype='audio/wav')

if __name__ == '__main__':
    app.run()

