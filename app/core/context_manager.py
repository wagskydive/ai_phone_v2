import os


class ContextManager:
    """Simple context store with optional persistence."""

    def __init__(self, storage_path: str | None = None):
        self.storage_path = storage_path
        self.history: list[str] = []
        if self.storage_path and os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                self.history = [line.strip() for line in f if line.strip()]

    def add_entry(self, text: str) -> None:
        self.history.append(text)
        if self.storage_path:
            with open(self.storage_path, "a") as f:
                f.write(text + "\n")

    def summarize(self) -> str:
        """Return concatenated summary for now."""
        return " ".join(self.history[-5:])

