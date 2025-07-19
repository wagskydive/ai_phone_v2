from behave import given, when, then
import tempfile
import os

from tests.audio_utils import write_hello_wav

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
    write_hello_wav('/tmp/input.wav')
    context.handler.handle('/tmp/input.wav')

@when('I process another audio file')
def step_when_process_another_audio(context):
    write_hello_wav('/tmp/input.wav')
    context.handler.handle('/tmp/input.wav')

@then('the memory file contains the transcription and reply')
def step_then_memory_file_contents(context):
    with open(context.memory_file, 'r') as f:
        contents = f.read()
    assert 'Hello' in contents
    assert 'You said: Hello' in contents
    os.unlink(context.memory_file)

@then('the memory file contains two summaries')
def step_then_two_summaries(context):
    with open(context.memory_file, 'r') as f:
        lines = f.readlines()
    summary_lines = [ln for ln in lines if ln.startswith('SUMMARY:')]
    assert len(summary_lines) >= 2
    os.unlink(context.memory_file)

@when('I process an audio file with interruption')
def step_when_process_with_interrupt(context):
    write_hello_wav('/tmp/input.wav')
    context.audio = context.handler.handle('/tmp/input.wav', interrupt_fn=lambda: True)

@then('no audio is returned')
def step_then_no_audio(context):
    assert context.audio == b''
