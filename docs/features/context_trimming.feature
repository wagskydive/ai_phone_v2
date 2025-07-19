Feature: Context Trimming
  Old conversation entries are trimmed to keep memory small.

  Scenario: Trim history when it grows
    Given a context manager with history longer than limit
    When trimming is invoked
    Then only the most recent entries remain
