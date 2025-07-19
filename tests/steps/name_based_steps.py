from behave import given, when, then
from tests.audio_utils import write_hello_wav


@then('the caller name should be "{name}"')
def step_then_caller_name(context, name):
    assert context.manager.caller_name == name


@when('the caller says "{text}"')
def step_when_caller_says(context, text):
    # stub ASR to return provided text
    context.handler.asr.transcribe = lambda _: text
    write_hello_wav('/tmp/input.wav')
    context.handler.handle('/tmp/input.wav')


@when('I process another audio saying "{text}"')
def step_when_process_another_saying(context, text):
    context.handler.asr.transcribe = lambda _: text
    write_hello_wav('/tmp/input.wav')
    context.handler.handle('/tmp/input.wav')
    context.last_reply = context.handler.last_reply


@then('the reply includes "{text}"')
def step_then_reply_includes(context, text):
    assert text in context.last_reply
