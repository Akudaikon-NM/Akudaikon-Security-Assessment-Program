from pathlib import Path
import sys
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from extract_questions import synthesize_questions

MODULE_DIR = Path("control_library/modules")

def main():
    changed = 0
    for p in sorted(MODULE_DIR.glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        qs = data.get("questions") or []
        if len(qs) == 0:
            data["questions"] = synthesize_questions(data)
            data.setdefault("__meta__", {})
            data["__meta__"]["questions_source"] = "synthesized"
            p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
            changed += 1
            print(f"✓ Enriched {p.name}")
    print(f"\nEnriched {changed} modules with synthesized questions.")

if __name__ == "__main__":
    main()
