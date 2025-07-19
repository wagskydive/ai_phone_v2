from __future__ import annotations

import os
import re

from app.modules.llm import BaseLLM


class ContextManager:
    """Simple context store with optional persistence and trimming."""

    SUMMARY_PREFIX = "SUMMARY: "
    NAME_PREFIX = "NAME: "

    def __init__(self, storage_path: str | None = None, memory_limit: int | None = None, llm: BaseLLM | None = None):
        self.storage_path = storage_path
        self.memory_limit = memory_limit
        self.llm = llm
        self.caller_name: str | None = None
        # per-call history
        self.history: list[str] = []
        # summaries of previous calls
        self.past_summaries: list[str] = []
        if self.storage_path and os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(self.NAME_PREFIX):
                        self.caller_name = line[len(self.NAME_PREFIX) :]
                        continue
                    if line.startswith(self.SUMMARY_PREFIX):
                        self.past_summaries.append(
                            line[len(self.SUMMARY_PREFIX) :]
                        )
                    else:
                        # treat plain lines from older files as summaries
                        self.past_summaries.append(line)

    def _summarize_entries(self, entries: list[str]) -> str:
        """Summarize a list of text entries using the configured LLM."""
        text = " ".join(entries)
        if self.llm:
            try:
                return self.llm.summarize(text)
            except Exception:
                # fallback to raw text on failure
                pass
        return text

    def _extract_name(self, text: str) -> str | None:
        """Return a caller name found in ``text`` using the LLM if available."""
        if self.llm and hasattr(self.llm, "extract_name"):
            try:
                name = self.llm.extract_name(text)
                if name:
                    return name
            except Exception:
                pass
        text = text.lower()
        patterns = [
            r"my name is ([a-zA-Z]+)",
            r"i am ([a-zA-Z]+)",
            r"i'm ([a-zA-Z]+)",
            r"this is ([a-zA-Z]+)",
        ]
        for pat in patterns:
            match = re.search(pat, text)
            if match:
                return match.group(1).capitalize()
        return None

    def set_caller_name(self, name: str) -> None:
        """Persist and store the caller name."""
        self.caller_name = name
        if self.storage_path:
            with open(self.storage_path, "a") as f:
                f.write(f"{self.NAME_PREFIX}{name}\n")

    def add_entry(self, text: str) -> None:
        if self.caller_name is None:
            name = self._extract_name(text)
            if name:
                self.set_caller_name(name)
        self.history.append(text)
        if self.storage_path:
            with open(self.storage_path, "a") as f:
                f.write(text + "\n")
        # trim history if needed after adding new entry
        self.trim_history()

    def trim_history(self, limit: int | None = None) -> None:
        """Trim stored history to at most ``limit`` entries."""
        limit = limit if limit is not None else self.memory_limit
        if limit is not None and len(self.history) > limit:
            excess = self.history[:-limit]
            if excess:
                summary = self._summarize_entries(excess)
                if self.storage_path:
                    with open(self.storage_path, "a") as f:
                        f.write(f"{self.SUMMARY_PREFIX}{summary}\n")
                self.past_summaries.append(summary)
            self.history = self.history[-limit:]

    def summarize(self) -> str:
        """Return a summary of recent history."""
        return self._summarize_entries(self.history[-5:])

    def get_context(self) -> str:
        """Return prompt including past summaries and current history."""
        return " ".join(self.past_summaries[-5:] + self.history[-5:])

    def save_summary(self) -> None:
        """Persist summary of current history and reset it."""
        summary = self._summarize_entries(self.history)
        if self.storage_path:
            with open(self.storage_path, "a") as f:
                f.write(f"{self.SUMMARY_PREFIX}{summary}\n")
        self.past_summaries.append(summary)
        self.history.clear()

