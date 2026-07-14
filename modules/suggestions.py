"""
Password Suggestions Generator.
Generates actionable, human-readable suggestions based on which checks failed.
"""


def generate_suggestions(password, policy_result, common_result, dict_result,
                          keyboard_result, repeat_result, sequence_result, entropy_value) -> list:
    suggestions = []

    if common_result["is_common"]:
        suggestions.append("This password appears in known breach/common password lists. Change it immediately.")

    if dict_result["vulnerable"]:
        suggestions.append(
            f"Avoid using dictionary words like '{dict_result['matched_word']}' -- "
            "even with number/symbol substitutions, these are easily cracked."
        )

    if keyboard_result["detected"]:
        suggestions.append(
            f"Avoid keyboard-walk patterns like '{keyboard_result['pattern']}' -- these are among the first "
            "patterns attackers try."
        )

    if repeat_result["detected"]:
        suggestions.append(
            f"Avoid repeating the same character, e.g. '{repeat_result['pattern']}' -- this reduces randomness significantly."
        )

    if sequence_result["detected"]:
        suggestions.append(
            f"Avoid sequential characters like '{sequence_result['pattern']}' -- these are trivial to guess."
        )

    if not policy_result["length"]:
        suggestions.append(
            f"Increase your password length to at least {policy_result['min_length_required']} characters "
            f"(currently {policy_result['actual_length']})."
        )

    if not policy_result["uppercase"]:
        suggestions.append("Add at least one uppercase letter (A-Z).")

    if not policy_result["lowercase"]:
        suggestions.append("Add at least one lowercase letter (a-z).")

    if not policy_result["numbers"]:
        suggestions.append("Add at least one number (0-9).")

    if not policy_result["special"]:
        suggestions.append("Add at least one special character (e.g. ! @ # $ % ^ & *).")

    if entropy_value < 60 and not suggestions:
        suggestions.append("Consider increasing password length further to boost overall entropy/randomness.")

    if len(password) < 16:
        suggestions.append("For maximum security, aim for 16+ characters -- consider using a passphrase of 4-5 random words.")

    suggestions.append("Never reuse this password across multiple accounts/sites.")
    suggestions.append("Consider using a password manager to generate and store strong unique passwords.")

    return suggestions
