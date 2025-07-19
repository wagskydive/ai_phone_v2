from behave import given, when, then
from app.modules.tts_piper import PiperTTS

@given('the text "{text}"')
def step_given_text(context, text):
    context.tts_text = text

@when('the TTS module synthesizes the text')
def step_when_tts(context):
    tts = PiperTTS()
    context.audio_bytes = tts.synthesize(context.tts_text)

@then('audio bytes are produced')
def step_then_audio_bytes(context):
    assert isinstance(context.audio_bytes, (bytes, bytearray))
    assert len(context.audio_bytes) > 0

@then('the audio length is greater than {length:d}')
def step_then_audio_length(context, length: int):
    assert len(context.audio_bytes) > length
