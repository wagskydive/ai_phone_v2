from behave import given, when, then
from app.modules.asr_whisper import WhisperASR
from app.modules.llm_ollama import OllamaLLM
from app.modules.tts_piper import PiperTTS

@given('a voice input saying "{text}"')
def step_given_voice_input(context, text):
    context.audio_path = '/tmp/input.wav'
    context.input_text = text

@when('the ASR transcribes it')
def step_when_transcribe(context):
    asr = WhisperASR()
    context.transcribed = asr.transcribe(context.audio_path)

@when('the LLM generates a response')
@then('the LLM generates a response')
def step_when_llm_response(context):
    llm = OllamaLLM()
    context.response = llm.generate(context.transcribed)

@then('the TTS returns playable audio')
def step_then_tts_audio(context):
    tts = PiperTTS()
    audio = tts.synthesize(context.response)
    assert isinstance(audio, (bytes, bytearray))

