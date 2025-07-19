Feature: ASR module
  Scenario: Placeholder ASR returns transcription
    Given an audio file at "/tmp/input.wav"
    When the ASR module processes the audio
    Then a transcription string is returned
