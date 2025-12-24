# tools/pdf_to_module.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

from pypdf import PdfReader

# Import question synthesis and normalization
sys.path.insert(0, str(Path(__file__).parent))
from extract_questions import synthesize_questions, normalize_questions


HEADER_PATTERNS = [
    r"^Objective:",
    r"^Area of Focus:",
    r"^What Needs to Be in the Report",
    r"^Document Review List:",
    r"^Positive Findings:",
    r"^Negative Findings:",
    r"^Stmt\s+\d+(\.\d+)?:",   # e.g., Stmt 2.1:
]

SECTION_START_RE = re.compile(r"^(Stmt\s+\d+(\.\d+)?:\s+.+)$", re.MULTILINE)


def extract_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    pages = []
    for p in reader.pages:
        t = p.extract_text() or ""
        pages.append(t)
    # normalize
    text = "\n".join(pages)
    text = text.replace("\u00ad", "")  # soft hyphen
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _grab_block(text: str, start_label: str, next_labels: List[str]) -> str:
    """
    Returns text after `start_label` up to the earliest next label occurrence.
    """
    start_idx = text.find(start_label)
    if start_idx == -1:
        return ""
    start_idx = start_idx + len(start_label)

    # find the nearest next label after start_idx
    candidates = []
    for lab in next_labels:
        j = text.find(lab, start_idx)
        if j != -1:
            candidates.append(j)
    end_idx = min(candidates) if candidates else len(text)
    return text[start_idx:end_idx].strip()


def _bullets_from_block(block: str) -> List[str]:
    # Handles "o " bullets and "•" bullets and "▪"
    lines = [ln.strip() for ln in block.splitlines()]
    out = []
    for ln in lines:
        ln = ln.strip("•").strip()
        ln = re.sub(r"^[o▪\-]\s+", "", ln).strip()
        if not ln:
            continue
        # avoid obvious page/footer artifacts
        if re.search(r"Page\s+\d+", ln):
            continue
        out.append(ln)
    # de-dup while preserving order
    seen = set()
    deduped = []
    for x in out:
        if x not in seen:
            deduped.append(x)
            seen.add(x)
    return deduped


def split_into_statement_sections(text: str) -> List[Dict[str, str]]:
    """
    Splits the PDF text into sections starting at 'Stmt X.Y:' headers.
    Returns list of dicts: { "header": "...", "body": "..." }
    """
    matches = list(SECTION_START_RE.finditer(text))
    if not matches:
        return []
    sections = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        header = m.group(1).strip()
        body = text[m.end():end].strip()
        sections.append({"header": header, "body": body})
    return sections


def build_module_from_pdf(pdf_path: str, module_stem: str) -> Dict[str, Any]:
    text = extract_pdf_text(pdf_path)

    # Title: prefer filename-ish fallback; or parse if you have consistent title headers
    title = module_stem.replace("_", " ").title()

    # Top-level objective: if present
    objective = ""
    if "Objective:" in text:
        objective = _grab_block(
            text,
            "Objective:",
            ["Area of Focus:", "What Needs", "Document Review List:", "Positive Findings:", "Negative Findings:", "Stmt "]
        )

    # Statements become questions + criteria + evidence
    statement_sections = split_into_statement_sections(text)

    evaluation_criteria: List[str] = []
    required_evidence: List[str] = []
    questions: List[Dict[str, Any]] = []

    for sec in statement_sections:
        header = sec["header"]
        body = sec["body"]

        # Objective per statement
        obj = _grab_block(
            body,
            "Objective:",
            ["Area of Focus:", "What Needs", "Document Review List:", "Positive Findings:", "Negative Findings:"]
        )

        # What needs to be in report / requirements list (good question source)
        what = ""
        # this label varies a bit; handle both "What Needs…" and generic "What Needs to Be…"
        m = re.search(r"(What Needs to Be.*?:)", body)
        if m:
            what_label = m.group(1)
            what = _grab_block(
                body,
                what_label,
                ["Document Review List:", "Positive Findings:", "Negative Findings:"]
            )

        docs = _grab_block(
            body,
            "Document Review List:",
            ["Positive Findings:", "Negative Findings:"]
        )

        pos = _grab_block(body, "Positive Findings:", ["Negative Findings:"])
        neg = _grab_block(body, "Negative Findings:", ["Stmt ", "CORE+ Statements", "Rating Criteria", "Step "])

        # Normalize to bullets
        what_items = _bullets_from_block(what)
        doc_items = _bullets_from_block(docs)
        pos_items = _bullets_from_block(pos)
        neg_items = _bullets_from_block(neg)

        # Collect at module level
        required_evidence.extend(doc_items)

        # Evaluation criteria: combine objective + positive findings expectations
        if obj:
            evaluation_criteria.append(f"{header} — {obj}")
        evaluation_criteria.extend([f"{header} — {x}" for x in pos_items if x])

        # Questions: "requirements" + "negative finding checks"
        q_list = []
        for item in what_items:
            q_list.append(f"Does the program/report include: {item}?")
        for item in neg_items:
            q_list.append(f"Verify this gap is not present: {item}.")

        # Fallback if PDF section lacks "What Needs…" bullets
        if not q_list and obj:
            q_list = [f"Validate: {obj}"]

        questions.append({
            "id": re.sub(r"[^A-Za-z0-9_.-]+", "_", header.split(":")[0]).strip("_"),
            "prompt": header,
            "checks": q_list,
            "evidence": doc_items,
        })

    # De-dup module lists
    def dedupe(seq: List[str]) -> List[str]:
        seen = set()
        out = []
        for x in seq:
            x = x.strip()
            if not x or x in seen:
                continue
            out.append(x)
            seen.add(x)
        return out

    evaluation_criteria = dedupe(evaluation_criteria)
    required_evidence = dedupe(required_evidence)

    module = {
        "module_id": module_stem,
        "title": title,
        "control_objective": objective or "Objective extracted from PDF statements.",
        "evaluation_criteria": evaluation_criteria,
        "required_evidence": required_evidence,
        "questions": questions,
        "__source_pdf__": pdf_path,
    }
    
    # After extraction, normalize and check if we got meaningful questions
    extracted_qs = normalize_questions(module.get("questions") or [])
    
    # Only synthesize if extraction produced nothing useful after normalization
    if not extracted_qs:
        module["questions"] = synthesize_questions(module)
        questions_source = "synthesized"
    else:
        module["questions"] = extracted_qs
        questions_source = "pdf"
    
    # Track provenance so you can tell what happened later
    module.setdefault("__meta__", {})
    module["__meta__"]["questions_source"] = questions_source
    
    return module
