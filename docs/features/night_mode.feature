Feature: Night Mode
  Scenario: Calls are blocked outside configured hours
    Given a scheduler with interval 0 and jitter 0
    And call window hours start 9 end 17
    And current hour is 3
    When I check if it should call now
    Then it returns False
