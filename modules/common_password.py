"""
Common Password Detection.
Checks the given password (case-insensitive) against a list of the most
commonly breached/used passwords (loaded from data/common_passwords.txt).
"""

import os

_cache = None


def _load_common_passwords(filepath: str) -> set:
    global _cache
    if _cache is not None:
        return _cache

    passwords = set()
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip().lower()
                if line:
                    passwords.add(line)
    _cache = passwords
    return passwords


def is_common_password(password: str, filepath: str) -> dict:
    common_set = _load_common_passwords(filepath)
    lowered = password.lower()

    is_common = lowered in common_set

    return {
        "is_common": is_common,
        "message": "This is one of the most commonly breached passwords in the world!" if is_common
                   else "Not found in common password list.",
    }
