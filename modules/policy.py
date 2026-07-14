"""
Password Policy Checker.
Checks against a standard configurable policy (length, uppercase, lowercase,
digits, special characters).
"""

import re

DEFAULT_POLICY = {
    "min_length": 12,
    "require_upper": True,
    "require_lower": True,
    "require_digit": True,
    "require_special": True,
}


def check_policy(password: str, policy: dict = None) -> dict:
    if policy is None:
        policy = DEFAULT_POLICY

    results = {
        "length": len(password) >= policy["min_length"],
        "uppercase": bool(re.search(r"[A-Z]", password)) if policy["require_upper"] else True,
        "lowercase": bool(re.search(r"[a-z]", password)) if policy["require_lower"] else True,
        "numbers": bool(re.search(r"[0-9]", password)) if policy["require_digit"] else True,
        "special": bool(re.search(r"[^a-zA-Z0-9]", password)) if policy["require_special"] else True,
    }

    results["actual_length"] = len(password)
    results["min_length_required"] = policy["min_length"]
    results["passed_count"] = sum(1 for k, v in results.items() if k in
                                   ("length", "uppercase", "lowercase", "numbers", "special") and v)
    results["total_checks"] = 5
    results["all_passed"] = results["passed_count"] == results["total_checks"]

    return results
