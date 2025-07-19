Feature: Context Summarization
  The system condenses conversation history for efficient storage.

  Scenario: Summarize last statements
    Given a context manager with history
    When I request a summary
    Then a combined string of recent statements is returned
