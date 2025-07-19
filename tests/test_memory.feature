Feature: Memory module
  Scenario: Context manager summarizes history
    Given a new context manager
    When I add "Hello" to memory
    And I add "How are you?" to memory
    Then the summary contains "Hello"
    And the summary contains "How are you?"

  Scenario: Persistent memory saved to disk
    Given a context manager with persistent storage
    When I add "Persistent" to memory
    And I reload the context manager
    Then the summary contains "Persistent"
