from behave import given, when, then
import io
from app import server
from tests.audio_utils import write_hello_wav

class DummyHandler:
    def handle(self, path: str) -> bytes:
        return b"dummy"

@given('the server application')
def step_given_server(context):
    server.handler = DummyHandler()
    context.client = server.app.test_client()

@given('a sample audio file')
def step_given_audio(context):
    context.audio_path = '/tmp/upload.wav'
    write_hello_wav(context.audio_path)

@when('I post the audio to "{endpoint}"')
def step_when_post_audio(context, endpoint):
    with open(context.audio_path, 'rb') as f:
        data = {'audio': (io.BytesIO(f.read()), 'input.wav')}
        context.response = context.client.post(endpoint, data=data, content_type='multipart/form-data')

@then('the response contains synthesized audio')
def step_then_response_audio(context):
    assert context.response.status_code == 200
    assert len(context.response.data) > 0
