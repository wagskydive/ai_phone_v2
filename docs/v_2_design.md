# AI Phone System v2 - Design Document

## Overview
This document outlines the design and architecture of AI Phone System v2. The system integrates Whisper for speech recognition, an LLM (via Ollama) for natural conversation, and modular TTS backends for speech synthesis. It is optimized for both inbound and outbound phone call interactions over a SIP/analog hybrid setup, with character memory, call scheduling, and voice-based interruption handling.

---

## Goals
- Fully modular architecture for swappable components (ASR, LLM, TTS)
- Support multiple unique characters, each with persistent memory
- Summarize call context to maintain continuity while managing memory size
- Enable voice-based interruption (barge-in)
- Schedule outbound calls to internal extensions with randomness and night-time restriction
- Design using BDD methodology: documentation, tests, and then code

---

## Folder Structure
```
ai_phone_v2/
├── README.md
├── v2-design.md
├── v2-bdd-guide.md
├── features/
│   ├── inbound_calls.feature
│   ├── outbound_calls.feature
│   ├── memory_management.feature
│   └── interruptions.feature
├── characters/
│   ├── char_700/
│   │   ├── voice/
│   │   │   ├── model.onnx
│   │   │   └── config.json
│   │   └── memory.txt
│   └── char_701/
├── modules/
│   ├── asr_whisper.py
│   ├── llm_ollama.py
│   ├── tts_piper.py
│   └── scheduler.py
├── core/
│   ├── call_handler.py
│   ├── context_manager.py
│   └── config.py
├── tests/
│   └── unit/
├── server.py
└── requirements.txt
```

---

## Modules

### ASR (Speech-to-Text)
- `asr_whisper.py`
- Converts incoming audio to text
- Performs resampling and audio cleanup

### TTS (Text-to-Speech)
- Multiple TTS modules like Piper or Chatterbox
- Generate and save PCM-compatible audio files

### LLM (Ollama)
- `llm_ollama.py`
- Sends prompt with current context and retrieves reply
- Context includes call summary from previous conversations

### Context Manager
- Stores per-character memory (conversation summaries)
- Appends new summarized call data
- Summaries are written to disk prefixed with `SUMMARY:` so later calls can
  reference prior conversations
- Uses summarization to avoid unbounded memory growth
- Summaries are now generated using the Ollama LLM

### Scheduler
- Triggers outbound calls to extensions 601-608
- Adds randomness to call timing (~ every 30 min)
- Restricts calling to daytime hours

### Call Handler
- Manages each call loop: record, transcribe, query, synthesize, play
- Interrupts AI playback if user starts speaking (barge-in)

---

## Key Features

### Modular Design
- Easy swapping of ASR, LLM, and TTS engines via config

### Characters
- Each has:
  - Dial-in extension (700-710)
  - Voice model and config
  - Persistent memory file for context

### Context Summarization
- After each call, the system summarizes the dialog using LLM
- Updates character memory
- LLM receives a compact context for continuity

### Voice-based Interruptions
- System monitors microphone during playback
- If user starts speaking, it stops TTS output
- Enhances conversational fluidity

### Outbound Call System
- Characters randomly call extensions 601-608
- Interval: ~30 minutes with jitter
- Calls only during defined daytime window

---

## Next Steps
1. Finalize README, config, and this document
2. Implement BDD tests from `features/`
3. Build out `core/` and `modules/`
4. Integrate with Asterisk/SIP hardware
5. Test with real analog phones

---

## Notes
- Uses `ffmpeg` for audio conversion
- Default sampling: 8000 Hz, mono, PCM
- All audio flows through `/tmp/` and is cleared after use
- Planned for expansion with internet calling and external API integrations

---

## Authors
- AI-assisted by ChatGPT
- Development by user

---

