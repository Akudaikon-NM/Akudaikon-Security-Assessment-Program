"""
Module loader for runner.
"""

import yaml
from pathlib import Path

REQUIRED_KEYS = ["title", "control_objective", "evaluation_criteria", "required_evidence"]

BASE_PATH = Path(__file__).resolve().parents[2] / "control_library" / "modules"

def load_module(module_filename_stem: str, strict: bool = False):
    """
    module_filename_stem must match the YAML filename without extension, e.g.
    '01_policies_and_procedures'
    
    If strict=True, raises ValueError for missing required keys instead of warnings.
    """
    path = BASE_PATH / f"{module_filename_stem}.yaml"
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        module_data = yaml.safe_load(f) or {}

    missing = [k for k in REQUIRED_KEYS if k not in module_data]
    if missing:
        if strict:
            raise ValueError(f"{module_filename_stem}.yaml missing required keys: {missing}")
        module_data["__warnings__"] = missing

    # helpful metadata
    module_data["__file__"] = str(path)
    module_data["__stem__"] = module_filename_stem
    # Optional module_id: default to filename stem for stability
    if "module_id" not in module_data:
        module_data["module_id"] = module_filename_stem

    return module_data


def list_modules():
    """
    Returns list of tuples: (filename_stem, display_title)
    Use filename_stem as the stable key for load_module().
    """
    modules = []
    if not BASE_PATH.exists():
        return modules

    for f in sorted(BASE_PATH.glob("*.yaml")):
        data = load_module(f.stem)
        if not data:
            continue

        # display title should be human-friendly
        display_title = data.get("title", f.stem)
        modules.append((f.stem, display_title))

    return modules