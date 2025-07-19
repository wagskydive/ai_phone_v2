Feature: TTS module
  Scenario: Placeholder TTS returns audio
    Given the text "Hello world"
    When the TTS module synthesizes the text
    Then audio bytes are produced
    And the audio length is greater than 0
