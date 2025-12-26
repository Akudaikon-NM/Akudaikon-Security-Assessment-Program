# apps/assessor_streamlit/scoring.py

from __future__ import annotations

from typing import Any, Dict, Tuple


WEIGHTS = {
    "yes": 1.0,
    "partial": 0.5,
    "no": 0.0,
    "n/a": None,   # ignored
    "na": None,    # sometimes users/type systems use NA
}


def _normalize_response(value: Any) -> str:
    if value is None:
        return "n/a"
    s = str(value).strip().lower()
    # normalize common variants
    if s in {"n/a", "na", "not applicable"}:
        return "n/a"
    if s in {"y", "yes"}:
        return "yes"
    if s in {"p", "partial", "partially", "in progress"}:
        return "partial"
    if s in {"n", "no"}:
        return "no"
    # default: treat unknown as N/A so it doesn't distort scoring
    return "n/a"


def calculate_score_percentage(responses: Dict[str, Any]) -> Tuple[float, int, int]:
    """
    Returns: (score_pct 0..1, answered_count, total_questions_seen)
    - answered_count excludes N/A
    - total_questions_seen includes all QIDs in responses
    """
    total_score = 0.0
    max_possible_score = 0.0

    total_questions_seen = 0
    answered_count = 0

    for qid, data in (responses or {}).items():
        total_questions_seen += 1

        if isinstance(data, dict):
            resp_raw = data.get("response", "N/A")
        else:
            # if responses somehow stores raw strings
            resp_raw = data

        resp = _normalize_response(resp_raw)
        weight = WEIGHTS.get(resp, None)

        # Ignore N/A
        if weight is None:
            continue

        total_score += float(weight)
        max_possible_score += 1.0
        answered_count += 1

    if max_possible_score == 0:
        return 0.0, 0, total_questions_seen

    return total_score / max_possible_score, answered_count, total_questions_seen


def generate_scorecard(module_data: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Minimal scorecard:
    - Overall Compliance: Pass / Partial / Fail / N/A
    - Compliance Score: numeric percent + debug counts
    """
    responses = (answers or {}).get("responses") or {}
    if not responses:
        return {
            "Overall Compliance": "N/A",
            "Compliance Score": "N/A",
        }

    score_pct, answered_count, total_questions_seen = calculate_score_percentage(responses)

    if answered_count == 0:
        overall = "N/A"
    elif score_pct >= 0.80:
        overall = "Pass"
    elif score_pct >= 0.50:
        overall = "Partial"
    else:
        overall = "Fail"

    return {
        "Overall Compliance": overall,
        "Compliance Score": f"{score_pct:.2f} ({int(round(score_pct * 100))}%)",
        "Answered (Non-N/A)": answered_count,
        "Questions Seen": total_questions_seen,
    }
