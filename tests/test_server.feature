Feature: HTTP server
  Scenario: Process uploaded audio
    Given the server application
    And a sample audio file
    When I post the audio to "/process"
    Then the response contains synthesized audio
