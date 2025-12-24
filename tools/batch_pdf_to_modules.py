# tools/batch_pdf_to_modules.py
import re
import sys
import yaml
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from pdf_to_module import build_module_from_pdf

PDF_DIR = Path("docs/source_pdfs")
OUT_DIR = Path("control_library/modules")

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s-]+", "_", s)
    return s

def parse_pdf_filename(pdf_path: Path):
    """
    Supports:
      '1. Policies and Procedures.pdf' -> (1, 'Policies and Procedures')
      '07 Training.pdf' -> (7, 'Training')  (optional)
    """
    name = pdf_path.stem

    m = re.match(r"^\s*(\d+)\.\s*(.+?)\s*$", name)
    if m:
        return int(m.group(1)), m.group(2)

    m = re.match(r"^\s*(\d+)\s+(.+?)\s*$", name)
    if m:
        return int(m.group(1)), m.group(2)

    return None, name  # fallback

def main():
    if not PDF_DIR.exists():
        print(f"Missing {PDF_DIR}")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {PDF_DIR}")
        sys.exit(1)

    for pdf in pdfs:
        size = pdf.stat().st_size
        if size == 0:
            print(f"SKIP (0 bytes): {pdf.name}")
            continue

        num, title = parse_pdf_filename(pdf)
        if num is not None:
            module_stem = f"{num:02d}_{slugify(title)}"
        else:
            module_stem = slugify(title)

        out_path = OUT_DIR / f"{module_stem}.yaml"

        print(f"\n=== {pdf.name} -> {out_path.name} ===")
        
        try:
            module = build_module_from_pdf(str(pdf), module_stem)
            # enforce stable naming
            module["module_id"] = module_stem
            module["title"] = module.get("title") or title

            # Write YAML
            with open(out_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(module, f, sort_keys=False, allow_unicode=True)
            
            print(f"✓ Created {out_path.name}")
        except Exception as e:
            print(f"✗ Failed to process {pdf.name}: {e}")
            continue

    print("\nDone. Generated/updated YAML modules in control_library/modules/")

if __name__ == "__main__":
    main()
