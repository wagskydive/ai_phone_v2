Feature: Modular TTS
  The system allows different TTS engines for unique voices.

  Scenario: Generate speech with the default TTS
    Given the text "Hello world"
    When the TTS module synthesizes the text
    Then audio bytes are produced
