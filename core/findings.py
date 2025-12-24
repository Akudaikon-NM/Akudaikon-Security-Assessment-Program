"""
Findings templates for consistent examiner-style output.
"""

from typing import Dict, List, Any

def generate_findings(module_data: Dict[str, Any], scorecard: Dict[str, Any]) -> List[str]:
    """Generate findings based on scorecard."""
    findings = []
    # Assume overall score from scorecard
    scores = list(scorecard.values())
    if all(s == 'Pass' for s in scores):
        template = module_data.get('finding_templates', {}).get('positive', 'Compliant.')
    elif any(s == 'Pass' for s in scores):
        template = module_data.get('finding_templates', {}).get('partial', 'Partial compliance.')
    else:
        template = module_data.get('finding_templates', {}).get('negative', 'Non-compliant.')
    findings.append(template)
    return findings