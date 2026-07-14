"""
Entropy calculation for passwords.
Entropy (bits) = length * log2(pool_size)
This estimates how many bits of "randomness" a password has, which is a
standard way (NIST / security literature) of approximating brute-force resistance.
"""

import math
import re


def get_char_pool_size(password: str) -> int:
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 32  # approx count of common special characters
    return pool if pool > 0 else 1


def calculate_entropy(password: str) -> float:
    if not password:
        return 0.0
    pool_size = get_char_pool_size(password)
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)


def entropy_rating(entropy: float) -> str:
    """Human-readable label for an entropy value."""
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Reasonable"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"


def estimate_crack_time(entropy: float, guesses_per_second: float = 1e10) -> str:
    """
    Rough offline brute-force time estimate assuming a powerful attacker
    (10 billion guesses/sec, typical for GPU-based offline attacks on weak hashes).
    Returns a human-readable string.
    """
    if entropy <= 0:
        return "Instantly"

    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_second

    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    elif seconds < 31536000 * 100:
        return f"{seconds/31536000:.1f} years"
    else:
        return "Centuries+"
