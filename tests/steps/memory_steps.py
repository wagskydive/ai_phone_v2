from behave import given, when, then
from app.core.context_manager import ContextManager
import tempfile

@given('a new context manager')
def step_given_new_context(context):
    context.manager = ContextManager()

@given('a context manager with history')
def step_given_context_with_history(context):
    context.manager = ContextManager()
    context.manager.add_entry("Hello")
    context.manager.add_entry("How are you?")

@given('a context manager with history longer than limit')
def step_given_history_longer(context):
    """Create a manager with more than two entries."""
    context.manager = ContextManager()
    context.manager.add_entry("Hello")
    context.manager.add_entry("How are you?")
    context.manager.add_entry("Goodbye")

@when('I add "{text}" to memory')
def step_when_add_memory(context, text):
    context.manager.add_entry(text)

@when('I request a summary')
def step_when_request_summary(context):
    context.summary = context.manager.summarize()

@when('trimming is invoked')
def step_when_trimming(context):
    context.manager.trim_history(2)

@then('the summary contains "{text}"')
def step_then_summary_contains(context, text):
    summary = context.manager.get_context()
    assert text in summary

@then('a combined string of recent statements is returned')
def step_then_combined_string(context):
    assert isinstance(context.summary, str)
    assert len(context.summary) > 0

@then('only the most recent entries remain')
def step_then_recent_entries(context):
    assert len(context.manager.history) <= 2


@given('a context manager with persistent storage')
def step_given_persistent_context(context):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    context.storage_file = tmp.name
    context.manager = ContextManager(storage_path=context.storage_file)


@when('I reload the context manager')
def step_when_reload_context(context):
    context.manager = ContextManager(storage_path=context.storage_file)
