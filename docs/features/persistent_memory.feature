Feature: Persistent Memory
  Characters maintain memory across calls using summaries.

  Scenario: Summarize recent conversation
    Given a new context manager
    When I add "Hello" to memory
    And I add "How are you?" to memory
    Then the summary should contain "Hello"
    And the summary should contain "How are you?"
