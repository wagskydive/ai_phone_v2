Feature: Call handler persistence
  Scenario: CallHandler persists conversation to disk
    Given a call handler with persistent memory
    When I process an audio file
    Then the memory file contains the transcription and reply
