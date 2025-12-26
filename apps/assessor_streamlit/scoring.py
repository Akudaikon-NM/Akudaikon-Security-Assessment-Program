# In scoring.py

def calculate_score_percentage(responses: Dict[str, Any]) -> float:
    total_score = 0.0
    max_possible_score = 0.0

    for qid, data in responses.items():
        resp = data.get("response", "N/A")
        
        weight = 0.0
        if resp == "Yes":
            weight = 1.0
        elif resp == "Partial":
            weight = 0.5
        elif resp == "No":
            weight = 0.0
        # N/A is handled below
        
        if resp != "N/A":
            total_score += weight
            max_possible_score += 1.0

    if max_possible_score == 0:
        return 0.0
    return total_score / max_possible_score

def generate_scorecard(module_data: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
    # This now scores the module based on question responses
    if not answers.get("responses"):
        return {"Overall": "N/A"}
    
    score_pct = calculate_score_percentage(answers["responses"])
    
    # Map percentage to compliance level (simple pass/partial/fail rule)
    if score_pct >= 0.8:
        overall_score = 'Pass'
    elif score_pct >= 0.5:
        overall_score = 'Partial'
    else:
        overall_score = 'Fail'
        
    # The scorecard now shows the calculated score and the percentage (for debug/completeness)
    return {
        "Overall Compliance": overall_score,
        "Compliance Score": f"{score_pct:.2f} ({int(score_pct * 100)}%)"
    }
# Note: You can remove the old score_module function as it's no longer necessary.
