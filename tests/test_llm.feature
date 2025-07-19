Feature: AI responds appropriately
  Scenario: Simple transcription and reply
    Given a voice input saying "Hello"
    When the ASR transcribes it
    And the LLM generates a response
    Then the TTS returns playable audio