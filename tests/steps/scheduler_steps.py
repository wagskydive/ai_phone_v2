from behave import given, when, then
from datetime import datetime

from app.modules.scheduler import CallScheduler

@given('a scheduler with interval {minutes:d} and jitter {jitter:d}')
def step_given_scheduler(context, minutes, jitter):
    context.scheduler = CallScheduler()
    # override loaded config
    context.scheduler.config['enabled'] = True
    context.scheduler.config['call_interval_minutes'] = minutes
    context.scheduler.config['jitter_minutes'] = jitter
    context.scheduler.next_interval = context.scheduler._calculate_interval()
    context.scheduler.last_call = 0

@given('current hour is {hour:d}')
def step_given_current_hour(context, hour):
    context.scheduler.now_fn = lambda: datetime(2023, 1, 1, hour, 0, 0)

@given('call window hours start {start:d} end {end:d}')
def step_given_hours(context, start, end):
    context.scheduler.config['hours'] = {'start': start, 'end': end}

@when('I calculate the next interval')
def step_when_calc_interval(context):
    context.interval = context.scheduler._calculate_interval()

@then('the interval is between {low:d} and {high:d}')
def step_then_interval_range(context, low, high):
    assert low <= context.interval <= high

@when('I check if it should call now')
def step_when_should_call_now(context):
    context.should_call = context.scheduler.should_call_now()
    context.interval = context.scheduler.next_interval

@then('it returns True')
def step_then_returns_true(context):
    assert context.should_call is True

@then('it returns False')
def step_then_returns_false(context):
    assert context.should_call is False
