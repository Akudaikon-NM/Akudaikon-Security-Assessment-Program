from pathlib import Path
import re
from pypdf import PdfReader
import yaml

PDF_DIR = Path("docs/source_pdfs")
MODULE_DIR = Path("control_library/modules")
DRAFT_DIR = Path("control_library/modules/_drafts")
DRAFT_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf_text(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        chunks = []
        for page in reader.pages:
            t = page.extract_text() or ""
            chunks.append(t)
        return "\n".join(chunks)
    except Exception as e:
        print(f"Warning: Could not read {pdf_path.name}: {e}")
        return ""

def normalize_lines(text: str):
    # basic cleanup
    text = text.replace("\u00a0", " ")
    lines = [l.strip() for l in text.splitlines()]
    lines = [l for l in lines if l]
    return lines

def guess_bullets(lines):
    bullets = []
    for l in lines:
        if re.match(r"^(\-|\•|\*|\u2022)\s+", l):
            bullets.append(re.sub(r"^(\-|\•|\*|\u2022)\s+", "", l).strip())
    # fallback: lines that look like checklist items
    if len(bullets) < 10:
        for l in lines:
            if re.match(r"^(Q\d+(\.\d+)?\:)", l, re.I):
                bullets.append(l)
    # de-dupe while preserving order
    seen = set()
    out = []
    for b in bullets:
        if b not in seen:
            seen.add(b)
            out.append(b)
    return out

def bullets_to_questions(bullets, prefix="Q"):
    questions = []
    for i, b in enumerate(bullets[:80], start=1):  # cap drafts
        prompt = b
        prompt = re.sub(r"^Q\d+(\.\d+)?\:\s*", "", prompt, flags=re.I)
        prompt = prompt.rstrip(".")
        if not prompt.endswith("?"):
            prompt = prompt + "?"
        questions.append({
            "id": f"{prefix}-{i:02d}",
            "prompt": prompt,
            "reference": "",
            "evidence_requests": []
        })
    return questions

def load_existing_yaml(stem: str):
    p = MODULE_DIR / f"{stem}.yaml"
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}

def save_yaml(obj, path: Path):
    path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True), encoding="utf-8")

def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDFs found in {PDF_DIR}")

    for pdf in pdfs:
        stem = pdf.stem
        # map pdf name -> module yaml stem when they differ (appendix etc.)
        # default: same stem
        module_stem = stem

        existing = load_existing_yaml(module_stem)
        text = extract_pdf_text(pdf)
        lines = normalize_lines(text)
        bullets = guess_bullets(lines)

        draft = dict(existing)  # start from existing module
        draft.setdefault("title", existing.get("title", module_stem))
        draft.setdefault("description", existing.get("description", ""))
        draft.setdefault("control_objective", existing.get("control_objective", ""))
        draft.setdefault("evaluation_criteria", existing.get("evaluation_criteria", []))
        draft.setdefault("required_evidence", existing.get("required_evidence", []))

        # only draft questions if missing or empty
        if not draft.get("questions"):
            prefix = module_stem.split("_", 1)[0].upper() if "_" in module_stem else "Q"
            draft["questions"] = bullets_to_questions(bullets, prefix=prefix)

        out_path = DRAFT_DIR / f"{module_stem}.yaml"
        save_yaml(draft, out_path)
        print(f"Wrote draft: {out_path} (bullets found: {len(bullets)})")

if __name__ == "__main__":
    main()
