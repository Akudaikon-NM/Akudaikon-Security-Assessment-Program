from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Prefer pypdf (usually installed); if you have pdfplumber, it tends to be nicer.
def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(str(pdf_path))
        pages = []
        for p in reader.pages:
            txt = p.extract_text() or ""
            pages.append(txt)
        return "\n".join(pages)
    except Exception:
        # Optional fallback
        try:
            import pdfplumber  # type: ignore
            pages = []
            with pdfplumber.open(str(pdf_path)) as pdf:
                for page in pdf.pages:
                    pages.append(page.extract_text() or "")
            return "\n".join(pages)
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from {pdf_path.name}: {e}")


@dataclass
class ParsedQuestion:
    question: str
    evidence: Optional[str] = None
    reference: Optional[str] = None
    key_check: Optional[str] = None


def _clean(s: str) -> str:
    s = s.replace("\u25a1", "").replace("☐", "").strip()
    s = re.sub(r"\s+", " ", s)
    return s.strip("•- ").strip()


def parse_policies_and_procedures_pdf_to_module(text: str) -> Dict[str, Any]:
    """
    Tailored to the structure in '1. Policies and Procedures.pdf':
    - Numbered sections: '1. Governance and Oversight', '2. Access Controls and Authentication', ...
    - Within each section:
        Core Assessment:
        Positive Finding:
        Negative Finding:
        Questions:
          ☐ question...
          Evidence: ...
          Reference: ...
        Document Request:
          o ...
    - Later sections include Core+ topics with same pattern.
    """

    # Split into major numbered sections (1., 2., 3., ...)
    # Keep header line with the section.
    section_re = re.compile(r"(?m)^\s*(\d+)\.\s+([^\n]+)\s*$")
    matches = list(section_re.finditer(text))
    if not matches:
        raise ValueError("Could not find numbered sections like '1. Governance and Oversight'.")

    sections: List[Tuple[str, str]] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        header = f"{m.group(1)}. {m.group(2)}"
        body = text[start:end]
        sections.append((header, body))

    evaluation_criteria: List[str] = []
    required_evidence: List[str] = []
    questions: List[Dict[str, Any]] = []

    # Helpers
    def grab_block(label: str, blob: str) -> Optional[str]:
        # Gets text after 'Label:' until the next known label or section boundary.
        labels = [
            "Core Assessment:",
            "Core+ Assessment:",
            "Positive Finding:",
            "Negative Finding:",
            "Questions:",
            "Document Request:",
            "CORE Validation",
            "Core Review Summary",
            "Core+ Review Summary",
            "Rating Criteria Indicators",
            "Application of the Matrix",
            "Recommendations",
            "Remediation:",
        ]
        # Build a stop regex of any label
        stop = r"(?:" + "|".join(re.escape(x) for x in labels) + r")"
        pat = re.compile(rf"(?s){re.escape(label)}\s*(.*?)(?=\n\s*{stop}|\Z)")
        m = pat.search(blob)
        return m.group(1).strip() if m else None

    qline_re = re.compile(r"(?m)^\s*(?:☐|\[\s*\]|\-|\•)?\s*(Has|Are|Is|Do|Does|What|How|When|Who|Which)\b.*?$")

    for header, body in sections:
        # Core/Core+ Assessment bullets become evaluation criteria
        assess = grab_block("Core Assessment:", body) or ""
        assess2 = grab_block("Core+ Assessment:", body) or ""
        for blk in [assess, assess2]:
            for line in blk.splitlines():
                line = _clean(line)
                if not line:
                    continue
                # Many lines are "o Verified whether..." or "Evaluated..."
                # Keep them as criteria statements.
                evaluation_criteria.append(line)

        # Document Request bullets become required evidence
        docreq = grab_block("Document Request:", body) or ""
        for line in docreq.splitlines():
            line = _clean(line)
            if not line:
                continue
            # Skip stray single letters/bullets
            if len(line) < 3:
                continue
            required_evidence.append(line)

        # Questions block
        qblk = grab_block("Questions:", body) or ""
        if qblk:
            # Parse question lines + nearby Evidence/Reference/Key Check lines
            lines = [l.strip() for l in qblk.splitlines() if l.strip()]
            current: Optional[ParsedQuestion] = None

            def flush():
                nonlocal current
                if current and current.question:
                    questions.append(
                        {
                            "question": current.question,
                            **({"evidence": current.evidence} if current.evidence else {}),
                            **({"reference": current.reference} if current.reference else {}),
                            **({"key_check": current.key_check} if current.key_check else {}),
                            "area": header,
                        }
                    )
                current = None

            for raw in lines:
                s = _clean(raw)

                # Start of a new question
                if qline_re.match(s):
                    flush()
                    current = ParsedQuestion(question=s)
                    continue

                # Evidence / Reference / Key Check lines (often prefixed)
                if s.lower().startswith("evidence:"):
                    if current:
                        current.evidence = _clean(s.split(":", 1)[1])
                    continue
                if s.lower().startswith("reference:"):
                    if current:
                        current.reference = _clean(s.split(":", 1)[1])
                    continue
                if s.lower().startswith("key check:"):
                    if current:
                        current.key_check = _clean(s.split(":", 1)[1])
                    continue

                # Sometimes evidence/ref appear as "Evidence: ... Reference: ..."
                if "reference:" in s.lower() and "evidence:" in s.lower():
                    if current:
                        # naive split
                        parts = re.split(r"(?i)\breference:\b", s, maxsplit=1)
                        ev = re.split(r"(?i)\bevidence:\b", parts[0], maxsplit=1)[-1]
                        current.evidence = _clean(ev)
                        current.reference = _clean(parts[1])
                    continue

                # Otherwise treat as continuation text for the current question
                if current:
                    # append gently
                    current.question = _clean(current.question + " " + s)

            flush()

    # De-dupe, preserve order
    def dedupe(seq: List[str]) -> List[str]:
        seen = set()
        out = []
        for x in seq:
            k = x.strip().lower()
            if not k or k in seen:
                continue
            seen.add(k)
            out.append(x)
        return out

    evaluation_criteria = dedupe(evaluation_criteria)
    required_evidence = dedupe(required_evidence)

    # Build module
    module = {
        "title": "Policies and Procedures",
        "description": "Evidence-led review of the Information Security Program's governance, policies, and supporting procedures aligned to Appendix A to Part 748.",
        "control_objective": "Ensure the credit union maintains a board-approved, well-documented information security program with effective administrative, technical, and physical safeguards.",
        "evaluation_criteria": evaluation_criteria,
        "required_evidence": required_evidence,
        "questions": questions,
    }
    return module


def build_module_from_pdf(pdf_path: Path) -> Dict[str, Any]:
    text = extract_text_from_pdf(pdf_path)
    return parse_policies_and_procedures_pdf_to_module(text)


if __name__ == "__main__":
    import sys, yaml  # type: ignore

    pdf = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    module = build_module_from_pdf(pdf)
    with open(out, "w", encoding="utf-8") as f:
        yaml.safe_dump(module, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote: {out}")
