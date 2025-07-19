# Tickets

## T1 - Draft BDD tests and placeholder modules
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Create initial BDD test for LLM interaction and implement minimal placeholder modules and server skeleton as per docs.


## T2 - Implement core event loop and HTTP interface
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Add a simple scheduler-driven event loop in `app/main.py` and enhance
`scheduler.py` to read `schedule.json`. Update roadmap accordingly.

## T3 - Expand BDD tests for core modules
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Write additional BDD features covering ASR, TTS and memory modules as
outlined in `docs/features/` for future development.

## T4 - Implement core module skeletons
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Build initial ASR, TTS and LLM module classes with real method signatures as specified in `docs/v_2_design.md`. No external integrations yet.

## T5 - Add persistent memory support
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Extend `ContextManager` to optionally persist history to disk and integrate it with `CallHandler`. Add BDD scenario for persistent memory.

## T6 - Scheduler randomness and tests
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Enhance `CallScheduler` with configurable jitter to randomize call intervals and
add BDD scenarios covering scheduling logic.

## T7 - Night mode scheduling
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Restrict outbound calls to daytime hours using scheduler configuration and add
BDD scenarios verifying calls are blocked outside this window.

## T8 - Reference previous calls in context
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Enhance `ContextManager` and `CallHandler` so that the LLM prompt includes
summaries from previous calls. Add BDD tests ensuring past conversation
snippets are referenced when generating responses.

## T9 - Interruptible AI responses
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Implement voice activity detection to stop TTS playback when the caller
begins speaking. Write BDD scenarios verifying that playback halts when
input is detected mid-response.

## T10 - Schedule outbound call targets
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Implement dialing logic to call extensions 601-608 at randomized intervals as per schedule configuration.

## T11 - Memory pruning feature
- [x] Started
- [x] Behavior Written
- [x] Code Written
- [x] Tests Passed
- [x] Documentation Written

### Description
Add trimming capability to `ContextManager` with a `trim_history` method and new
BDD scenario ensuring old entries are removed when history exceeds a limit.
