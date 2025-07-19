Feature: Call scheduling
  Scenario: Interval includes jitter
    Given a scheduler with interval 30 and jitter 5
    When I calculate the next interval
    Then the interval is between 25 and 35

  Scenario: Call allowed after interval
    Given a scheduler with interval 0 and jitter 0
    When I check if it should call now
    Then it returns True

  Scenario: No call outside hours
    Given a scheduler with interval 0 and jitter 0
    And call window hours start 23 end 23
    And current hour is 3
    When I check if it should call now
    Then it returns False

  Scenario: Daytime call allowed within hours
    Given a scheduler with interval 0 and jitter 0
    And call window hours start 9 end 17
    And current hour is 10
    When I check if it should call now
    Then it returns True

  Scenario: Next interval randomized after call
    Given a scheduler with interval 30 and jitter 5
    When I check if it should call now
    Then it returns True
    And the interval is between 25 and 35
