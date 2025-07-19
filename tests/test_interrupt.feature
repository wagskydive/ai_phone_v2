Feature: Interruptible playback
  Scenario: Playback stops on user speech
    Given a call handler with persistent memory
    When I process an audio file with interruption
    Then no audio is returned
