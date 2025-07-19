import random
from typing import Sequence

class OutboundDialer:
    """Simple dialer that selects an extension to call."""

    def __init__(self, extensions: Sequence[int] | None = None) -> None:
        self.extensions = list(extensions or range(601, 609))

    def dial(self) -> int:
        """Return the chosen extension to dial. Actual telephony omitted."""
        extension = random.choice(self.extensions)
        # In real implementation we'd instruct Asterisk to dial here
        return extension
