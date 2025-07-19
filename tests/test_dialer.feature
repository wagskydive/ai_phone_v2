Feature: Outbound Dialer
  Scenario: Random extension selection
    Given a dialer configured for extensions 601 to 608
    When a call is placed
    Then the chosen extension is between 601 and 608
