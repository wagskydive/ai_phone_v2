from flask import Flask, request, send_file
import tempfile
import os
import requests
import whisper
import subprocess
import wave
import numpy as np

from piper.voice import PiperVoice

app = Flask(__name__)

# Load Whisper model for transcription
asr = whisper.load_model("base")

# Load Piper voice model (ensure the path is correct)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPER_MODEL = os.path.join(BASE_DIR, "en_GB-alan-medium.onnx")  # Replace with your model
voice = PiperVoice.load(PIPER_MODEL)


SYSTEM_PROMPT = "You are a sneaky bastard that tries to get under peoples skin. This is a phone call so please give short responses."




def convert_audio(input_path):
    cleaned_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    command = [
        "ffmpeg",
        "-y",                # overwrite output
        "-i", input_path,
        "-ac", "1",          # mono
        "-ar", "16000",      # 16kHz
        "-sample_fmt", "s16",# 16-bit PCM
        cleaned_path
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return cleaned_path
    except subprocess.CalledProcessError:
        print("[❌] Failed to convert audio")
        return None

@app.route('/process', methods=['POST'])
def process_audio():
    # Step 1: Save incoming audio
    input_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    with open(input_wav, "wb") as f:
        f.write(request.get_data())
    print(f"[📥] Audio received: {input_wav}")
    file_info = subprocess.getoutput(f"file {input_wav}")
    print(f"[ℹ️] Saved file info: {file_info}")
    

    # Step 2: Transcribe with Whisper
    try:
        converted_wav = convert_audio(input_wav)
        if not converted_wav:
            return "Audio conversion failed", 500
        result = asr.transcribe(converted_wav)
        user_text = result["text"].strip()
        print(f"[🗣️] You said: {user_text}")
    except Exception as e:
        print(f"[❌] Whisper error: {e}")
        return "Whisper error", 500

    # Step 3: Query LLM (Ollama)
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:latest",
            "prompt": user_text,
            "system": SYSTEM_PROMPT,
            "stream": False
        })
        try:
            ai_reply = res.json().get("response", "").strip()
            if not ai_reply:
                raise ValueError("No 'response' in LLM reply")
        except Exception as e:
            print(f"[❌] LLM parsing error: {e}")
            ai_reply = "Sorry, something went wrong with the AI response."
        print(f"[🤖] AI replied: {ai_reply}")
    except Exception as e:
        print(f"[❌] LLM error: {e}")
        ai_reply = "I'm sorry, I couldn't generate a response."

    # Step 4: Generate TTS with Piper
    try:
        wav_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        chunks = []
        sample_rate = None

        for chunk in voice.synthesize(ai_reply):
            arr = chunk.audio_float_array
            if sample_rate is None:
                sample_rate = chunk.sample_rate
            int16 = np.clip(arr * 32767, -32768, 32767).astype(np.int16)
            chunks.append(int16.tobytes())

        if not chunks:
            raise RuntimeError("Piper returned no audio")

        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            for data in chunks:
                wf.writeframes(data)

        print(f"[🔊] TTS audio saved: {wav_path}")
    except Exception as e:
        print(f"[❌] Piper TTS error: {e}")
        return "TTS error", 500


 

    # Step 5: Convert to .ulaw for Asterisk
    ulaw_path = os.path.join("/tmp", "ai_response.ulaw")
    convert_cmd = f"ffmpeg -y -i {wav_path} -ar 8000 -ac 1 -f mulaw {ulaw_path}"
    if os.system(convert_cmd) != 0:
        print(f"[❌] ffmpeg conversion failed: {convert_cmd}")
        return "Audio conversion error", 500

    print(f"[✅] Audio converted for Asterisk: {ulaw_path}")
    return send_file(ulaw_path, mimetype="audio/basic")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
 