"""
Password Score Engine.
Combines all individual checks (policy, entropy, common password,
dictionary attack, keyboard pattern, repeats, sequences) into a
single 0-100 score and a strength label.
"""

from modules.entropy import calculate_entropy, entropy_rating, estimate_crack_time
from modules.policy import check_policy
from modules.common_password import is_common_password
from modules.dictionary_attack import simulate_dictionary_attack
from modules.keyboard_pattern import detect_keyboard_pattern
from modules.repeat_detector import detect_repeated_chars
from modules.sequence_detector import detect_sequential_chars
from modules.suggestions import generate_suggestions


def analyze_password(password: str, common_pw_file: str, dictionary_file: str) -> dict:
    if not password:
        return {"error": "Password cannot be empty."}

    policy_result = check_policy(password)
    entropy_value = calculate_entropy(password)
    entropy_label = entropy_rating(entropy_value)
    crack_time = estimate_crack_time(entropy_value)

    common_result = is_common_password(password, common_pw_file)
    dict_result = simulate_dictionary_attack(password, dictionary_file)
    keyboard_result = detect_keyboard_pattern(password)
    repeat_result = detect_repeated_chars(password)
    sequence_result = detect_sequential_chars(password)

    # ---------- SCORING LOGIC (0-100) ----------
    score = 0

    # Policy checks: up to 40 points (8 points per check x 5 checks)
    score += policy_result["passed_count"] * 8

    # Entropy: up to 35 points, scaled (entropy of 90+ bits = full marks)
    entropy_points = min(35, round((entropy_value / 90) * 35))
    score += entropy_points

    # Length bonus: up to 10 points for length beyond the minimum
    length_bonus = min(10, max(0, (len(password) - 12) * 2))
    score += length_bonus

    # Penalties
    if common_result["is_common"]:
        score -= 40
    if dict_result["vulnerable"]:
        score -= 20
    if keyboard_result["detected"]:
        score -= 15
    if repeat_result["detected"]:
        score -= 15
    if sequence_result["detected"]:
        score -= 15

    score = max(0, min(100, round(score)))

    # ---------- STRENGTH LABEL ----------
    if score < 30:
        strength = "Very Weak"
    elif score < 50:
        strength = "Weak"
    elif score < 70:
        strength = "Moderate"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    suggestions = generate_suggestions(
        password=password,
        policy_result=policy_result,
        common_result=common_result,
        dict_result=dict_result,
        keyboard_result=keyboard_result,
        repeat_result=repeat_result,
        sequence_result=sequence_result,
        entropy_value=entropy_value,
    )

    return {
        "password_masked": "*" * len(password),
        "score": score,
        "strength": strength,
        "entropy": entropy_value,
        "entropy_label": entropy_label,
        "crack_time_estimate": crack_time,
        "policy": policy_result,
        "common_password": common_result,
        "dictionary_attack": dict_result,
        "keyboard_pattern": keyboard_result,
        "repeated_chars": repeat_result,
        "sequential_chars": sequence_result,
        "suggestions": suggestions,
    }
