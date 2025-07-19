from behave import given, when, then
from app.modules.dialer import OutboundDialer

@given('a dialer configured for extensions 601 to 608')
def step_given_dialer(context):
    context.dialer = OutboundDialer(list(range(601, 609)))

@when('a call is placed')
def step_when_call(context):
    context.extension = context.dialer.dial()

@then('the chosen extension is between 601 and 608')
def step_then_extension_range(context):
    assert 601 <= context.extension <= 608
