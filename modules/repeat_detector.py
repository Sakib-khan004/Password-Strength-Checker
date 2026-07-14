"""
Repeated Character Detection.
Detects runs of the same character repeated (e.g. aaaaaa, 111111, ------).
"""

import re

MIN_REPEAT_LENGTH = 4


def detect_repeated_chars(password: str) -> dict:
    match = re.search(r"(.)\1{" + str(MIN_REPEAT_LENGTH - 1) + r",}", password)

    if match:
        return {
            "detected": True,
            "pattern": match.group(0),
            "message": f"Repeated character sequence detected: '{match.group(0)}'",
        }

    return {"detected": False, "pattern": None, "message": "No repeated character sequence detected."}
