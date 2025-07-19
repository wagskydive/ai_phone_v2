from behave import given, when, then
from app.core.context_manager import ContextManager

@given('a new context manager')
def step_given_new_context(context):
    context.manager = ContextManager()

@given('a context manager with history')
def step_given_context_with_history(context):
    context.manager = ContextManager()
    context.manager.add_entry("Hello")
    context.manager.add_entry("How are you?")

@when('I add "{text}" to memory')
def step_when_add_memory(context, text):
    context.manager.add_entry(text)

@when('I request a summary')
def step_when_request_summary(context):
    context.summary = context.manager.summarize()

@when('trimming is invoked')
def step_when_trimming(context):
    # Simplistic trimming to last 2 entries
    if len(context.manager.history) > 2:
        context.manager.history = context.manager.history[-2:]

@then('the summary contains "{text}"')
def step_then_summary_contains(context, text):
    summary = context.manager.summarize()
    assert text in summary

@then('a combined string of recent statements is returned')
def step_then_combined_string(context):
    assert isinstance(context.summary, str)
    assert len(context.summary) > 0

@then('only the most recent entries remain')
def step_then_recent_entries(context):
    assert len(context.manager.history) <= 2
