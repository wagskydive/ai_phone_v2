import os


class ContextManager:
    """Simple context store with optional persistence and trimming."""

    SUMMARY_PREFIX = "SUMMARY: "

    def __init__(self, storage_path: str | None = None, memory_limit: int | None = None):
        self.storage_path = storage_path
        self.memory_limit = memory_limit
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
                    if line.startswith(self.SUMMARY_PREFIX):
                        self.past_summaries.append(
                            line[len(self.SUMMARY_PREFIX) :]
                        )
                    else:
                        # treat plain lines from older files as summaries
                        self.past_summaries.append(line)

    def add_entry(self, text: str) -> None:
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
            self.history = self.history[-limit:]

    def summarize(self) -> str:
        """Return concatenated summary for now."""
        return " ".join(self.history[-5:])

    def get_context(self) -> str:
        """Return prompt including past summaries and current history."""
        return " ".join(self.past_summaries[-5:] + self.history[-5:])

    def save_summary(self) -> None:
        """Persist summary of current history and reset it."""
        summary = self.summarize()
        if self.storage_path:
            with open(self.storage_path, "a") as f:
                f.write(f"{self.SUMMARY_PREFIX}{summary}\n")
        self.past_summaries.append(summary)
        self.history.clear()

