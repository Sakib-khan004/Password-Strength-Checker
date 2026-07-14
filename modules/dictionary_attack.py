"""
Dictionary Attack Simulation.
Simulates a basic dictionary attack: checks whether the password (or a close
variant of it, e.g. with common leetspeak substitutions or appended digits)
matches any word in a dictionary word list.
"""

import os
import re

_dict_cache = None

LEET_MAP = {
    "@": "a", "4": "a",
    "3": "e",
    "1": "i", "!": "i",
    "0": "o",
    "$": "s", "5": "s",
    "7": "t",
}


def _load_dictionary(filepath: str) -> set:
    global _dict_cache
    if _dict_cache is not None:
        return _dict_cache

    words = set()
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip().lower()
                if line:
                    words.add(line)
    _dict_cache = words
    return words


def _normalize_leet(word: str) -> str:
    result = word.lower()
    for leet_char, normal_char in LEET_MAP.items():
        result = result.replace(leet_char, normal_char)
    return result


def simulate_dictionary_attack(password: str, filepath: str) -> dict:
    words = _load_dictionary(filepath)
    lowered = password.lower()

    # 1. Direct match
    if lowered in words:
        return {"vulnerable": True, "matched_word": lowered, "method": "Direct match"}

    # 2. Strip trailing digits/special chars and check base word (e.g. "password123" -> "password")
    stripped = re.sub(r"[\d!@#$%^&*]+$", "", lowered)
    if stripped and stripped in words:
        return {"vulnerable": True, "matched_word": stripped, "method": "Base word with suffix"}

    # 3. Leetspeak normalization (e.g. "p@ssw0rd" -> "password")
    normalized = _normalize_leet(lowered)
    if normalized in words:
        return {"vulnerable": True, "matched_word": normalized, "method": "Leetspeak substitution"}

    normalized_stripped = re.sub(r"[\d!@#$%^&*]+$", "", normalized)
    if normalized_stripped and normalized_stripped in words:
        return {"vulnerable": True, "matched_word": normalized_stripped, "method": "Leetspeak + suffix"}

    return {"vulnerable": False, "matched_word": None, "method": None}
