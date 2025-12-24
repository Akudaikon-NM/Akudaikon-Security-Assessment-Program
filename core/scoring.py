"""
Scoring logic for assessment modules.
"""

import yaml
from typing import Dict, List, Any

def load_module(module_name: str) -> Dict[str, Any]:
    """Load a control module from YAML."""
    path = f"control_library/modules/{module_name}.yaml"
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def score_module(module_data: Dict[str, Any], answers: Dict[str, Any]) -> str:
    """Score a module: Pass/Partial/Fail based on answers."""
    # Placeholder: assume answers provide overall compliance
    compliance = answers.get('overall', 'unknown')
    if compliance == 'full':
        return 'Pass'
    elif compliance == 'partial':
        return 'Partial'
    else:
        return 'Fail'

def generate_scorecard(module_data: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
    """Generate scorecard by requirement."""
    score = score_module(module_data, answers)
    scorecard = {}
    for req in module_data.get('primary_requirements', []):
        scorecard[req] = score
    return scorecard