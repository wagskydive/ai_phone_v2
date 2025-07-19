from behave import given, when, then
import tempfile
import os

from app.core.call_handler import CallHandler
from app.modules.asr_whisper import WhisperASR
from app.modules.llm_ollama import OllamaLLM
from app.modules.tts_piper import PiperTTS

@given('a call handler with persistent memory')
def step_given_persistent_handler(context):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    context.memory_file = tmp.name
    context.handler = CallHandler(WhisperASR(), OllamaLLM(), PiperTTS(),
                                  storage_path=context.memory_file)

@when('I process an audio file')
def step_when_process_audio(context):
    context.handler.handle('/tmp/input.wav')

@then('the memory file contains the transcription and reply')
def step_then_memory_file_contents(context):
    with open(context.memory_file, 'r') as f:
        contents = f.read()
    assert 'Hello' in contents
    assert 'You said: Hello' in contents
    os.unlink(context.memory_file)
