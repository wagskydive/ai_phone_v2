Feature: Modular ASR
  The system supports pluggable ASR backends so implementations can be swapped.

  Scenario: Transcribe audio with the default ASR
    Given an audio file at "/tmp/input.wav"
    When the ASR module processes the audio
    Then a transcription string is returned
