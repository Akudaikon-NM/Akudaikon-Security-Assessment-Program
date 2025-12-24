# tools/write_module_yaml.py
import yaml
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from pdf_to_module import build_module_from_pdf

def write_module_yaml(pdf_path: str, module_stem: str, out_dir: str = "control_library/modules"):
    mod = build_module_from_pdf(pdf_path, module_stem)
    out_path = Path(out_dir) / f"{module_stem}.yaml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(mod, f, sort_keys=False, allow_unicode=True)
    return str(out_path)

if __name__ == "__main__":
    import sys
    pdf_path = sys.argv[1]
    module_stem = sys.argv[2]
    print(write_module_yaml(pdf_path, module_stem))
