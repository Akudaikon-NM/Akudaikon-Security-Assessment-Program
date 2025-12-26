"# findings.py
from typing import Any, Dict, List

def _as_list(x: Any) -> List[str]:
    """Normalize template content to a list of strings."""
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i) for i in x if i is not None]
    return [str(x)]

def generate_findings(module_data: Dict[str, Any], scorecard: Dict[str, Any]) -> List[str]:
    """
    Generate findings based on the overall compliance score from the scorecard.
    Expects scorecard["Overall Compliance"] in {"Pass","Partial","Fail","N/A"}.
    Looks for module_data["finding_templates"] keys: positive/partial/negative.
    """
    finding_templates = module_data.get("finding_templates", {}) or {}

    overall_score = (scorecard.get("Overall Compliance") or "N/A").strip()
    findings: List[str] = []

    if overall_score == "Pass":
        template = finding_templates.get("positive") or "The control domain is Compliant."
    elif overall_score == "Partial":
        template = finding_templates.get("partial") or "Partial compliance was noted."
    elif overall_score in ("Fail", "N/A"):
        template = finding_templates.get("negative") or "The control domain is Non-compliant."
    else:
        # unexpected value
        template = finding_templates.get("negative") or "The control domain is Non-compliant."

    findings.extend(_as_list(template))

    # Optional: add the computed score line if present
    score_pct = scorecard.get("Compliance Score")
    if score_pct:
        findings.append(f"Calculated Score: {score_pct}. This justifies the {overall_score} rating.")

    return findings
