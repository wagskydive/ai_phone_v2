Feature: Name based greetings
  Scenario: Caller name stored in context
    Given a new context manager
    When I add "My name is Alice" to memory
    Then the caller name should be "Alice"

  Scenario: Caller greeted by name on next call
    Given a call handler with persistent memory
    When the caller says "My name is Bob"
    And I process another audio saying "Hello"
    Then the reply includes "Hello Bob"

