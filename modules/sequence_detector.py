"""
Sequential Character Detection.
Detects ascending or descending sequences in letters or digits
(e.g. abcdef, fedcba, 123456, 654321).
"""

MIN_SEQUENCE_LENGTH = 4


def detect_sequential_chars(password: str) -> dict:
    lowered = password.lower()

    for start in range(len(lowered) - MIN_SEQUENCE_LENGTH + 1):
        chunk = lowered[start:start + MIN_SEQUENCE_LENGTH]

        if not (chunk.isalpha() or chunk.isdigit()):
            continue

        codes = [ord(c) for c in chunk]

        is_ascending = all(codes[i] + 1 == codes[i + 1] for i in range(len(codes) - 1))
        is_descending = all(codes[i] - 1 == codes[i + 1] for i in range(len(codes) - 1))

        if is_ascending or is_descending:
            direction = "ascending" if is_ascending else "descending"
            return {
                "detected": True,
                "pattern": chunk,
                "message": f"Sequential ({direction}) pattern detected: '{chunk}'",
            }

    return {"detected": False, "pattern": None, "message": "No sequential pattern detected."}
