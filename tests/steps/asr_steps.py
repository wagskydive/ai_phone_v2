from behave import given, when, then
from app.modules.asr_whisper import WhisperASR

@given('an audio file at "{path}"')
def step_given_audio_file(context, path):
    context.audio_path = path

@when('the ASR module processes the audio')
def step_when_asr_process(context):
    asr = WhisperASR()
    context.transcription = asr.transcribe(context.audio_path)

@then('a transcription string is returned')
def step_then_transcription(context):
    assert isinstance(context.transcription, str)
    assert context.transcription
