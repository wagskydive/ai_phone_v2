"""Minimal HTTP interface for call processing."""
from flask import Flask, request, jsonify

from app.modules.asr_whisper import WhisperASR
from app.modules.llm_ollama import OllamaLLM
from app.modules.tts_piper import PiperTTS
from app.core.call_handler import CallHandler

app = Flask(__name__)

asr = WhisperASR()
llm = OllamaLLM()
tts = PiperTTS()
handler = CallHandler(asr, llm, tts)

@app.route('/process', methods=['POST'])
def process():
    # In a real implementation audio data would be saved and processed
    audio_path = '/tmp/input.wav'
    audio = handler.handle(audio_path)
    return jsonify({'audio_bytes': len(audio)})

if __name__ == '__main__':
    app.run()

