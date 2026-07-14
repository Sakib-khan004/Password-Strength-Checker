"""
Keyboard Pattern Detection.
Detects passwords based on physical keyboard adjacency patterns
(e.g. qwerty, asdfgh, 123456, zxcvbn) rather than random typing.
"""

KEYBOARD_ROWS = [
    "`1234567890-=",
    "qwertyuiop[]\\",
    "asdfghjkl;'",
    "zxcvbnm,./",
]

MIN_PATTERN_LENGTH = 4


def _build_adjacency_sequences():
    sequences = []
    for row in KEYBOARD_ROWS:
        sequences.append(row)
        sequences.append(row[::-1])
    return sequences


_SEQUENCES = _build_adjacency_sequences()


def detect_keyboard_pattern(password: str) -> dict:
    lowered = password.lower()

    for seq in _SEQUENCES:
        for start in range(len(seq) - MIN_PATTERN_LENGTH + 1):
            chunk = seq[start:start + MIN_PATTERN_LENGTH]
            if chunk in lowered:
                return {
                    "detected": True,
                    "pattern": chunk,
                    "message": f"Keyboard walk pattern detected: '{chunk}'",
                }

    return {"detected": False, "pattern": None, "message": "No keyboard pattern detected."}
