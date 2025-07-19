class ContextManager:
    """Simple in-memory context store."""

    def __init__(self):
        self.history = []

    def add_entry(self, text: str) -> None:
        self.history.append(text)

    def summarize(self) -> str:
        """Return concatenated summary for now."""
        return " ".join(self.history[-5:])

