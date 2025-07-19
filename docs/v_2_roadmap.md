# AI Phone System V2 - Roadmap & Design

## Overview

This document outlines the roadmap, structure, and development methodology for Version 2 of the modular AI phone assistant system. This version focuses on modularity, maintainability, configurability, and expandability.

---

## 🌊 Goals
- Modular design for easy swapping of components (TTS, ASR, LLM)
- Multiple AI characters with individual configurations
- Persistent character memory with summarization
- Natural conversation handling, including interruption and memory referencing
- Outbound calling capability with randomized intervals
- Configurable scheduling to avoid outbound calls at night

---

## 🌿 Folder Structure
```
ai_phone_v2/
├── app/
│   ├── main.py
│   ├── config/
│   │   └── schedule.json
│   ├── modules/
│   │   ├── llm/
│   │   ├── tts/
│   │   ├── asr/
│   │   ├── memory/
│   │   └── dialer/
│   └── characters/
│       └── 700.json
├── tests/
│   ├── test_llm.feature
│   └── steps/
├── logs/
├── README.md
└── requirements.txt
```

---

## 🌟 Phase 1: Design & Planning
- [x] Define modular structure
- [x] Select tech stack and tools
- [x] Define configuration and memory architecture
- [x] Write roadmap and design documentation

---

## 🥺 Phase 2: BDD-Driven Test First Development
- [ ] Define BDD test features for core modules
- [ ] Add tests for:
  - LLM response flow
  - ASR transcription
  - TTS synthesis
  - Memory summarization
  - Outbound dialing logic
- [ ] Implement test stubs and mocks

Tools:
- `behave`
- `pytest` (optional)

---

## ⚙️ Phase 3: Core Modular Implementation

| Module       | Responsibility                                  |
|--------------|--------------------------------------------------|
| `asr/`       | Whisper-based transcription                     |
| `llm/`       | Query Ollama and manage conversation context    |
| `tts/`       | Generate speech using Piper/Chatterbox          |
| `memory/`    | Store, retrieve and summarize per-character mem |
| `dialer/`    | Outbound call scheduler and Asterisk interfacing|
| `characters/`| JSON configs per AI personality                 |

---

## 🌟 Phase 4: Features & Intelligence
- [ ] Summarize memory at end of call
- [ ] Reference previous calls (context aware)
- [ ] Interruptible AI responses using voice activity detection
- [ ] Schedule outbound calls to extensions 601-608
- [ ] Add randomness to call interval (avg every 30 minutes)
- [ ] Restrict call times (e.g., avoid night)
- [ ] Implement memory aging / pruning

---

## 📆 Suggested Timeline

| Week  | Focus Area                          |
|--------|-------------------------------------|
| Week 1 | Finalize BDD specs and test stubs   |
| Week 2 | Build ASR, TTS, LLM module shells   |
| Week 3 | Implement memory, config, schedules |
| Week 4 | Dialing + multi-character support   |
| Week 5 | Polish, interruptions, full testing |

---

## Next Steps
- [x] Draft initial BDD tests
- [x] Set up placeholder modules
- [x] Implement core event loop and HTTP interface

Let me know if you'd like to generate any starter files or templates next!

