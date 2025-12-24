#!/usr/bin/env python3
"""
Configuration-driven question extraction from PDF text.
Uses extract_profiles.yaml to define extraction rules per module.
Also includes question synthesis utilities for modules without explicit questions.
"""

import re
from pathlib import Path
from typing import List, Dict, Any
import yaml


def normalize_questions(qs):
    """
    Filter and normalize questions, removing junk like headers, footers, etc.
    """
    out = []
    for q in qs or []:
        s = " ".join(str(q).split())
        if len(s) < 10:
            continue
        # reject obvious noise
        if s.lower() in {"questions", "question", "n/a"}:
            continue
        out.append(s)
    # de-dupe preserving order
    seen = set()
    dedup = []
    for s in out:
        k = s.lower()
        if k not in seen:
            dedup.append(s)
            seen.add(k)
    return dedup


def synthesize_questions(module):
    """
    Generate assessment questions from evaluation_criteria and required_evidence.
    
    For each criterion/evidence item, generates 5 standard examiner questions:
    1. Existence - does it exist?
    2. Approval/Governance - who approved it?
    3. Implementation - how is it used?
    4. Evidence - what proves it?
    5. Review cadence - how often reviewed?
    """
    crit = module.get("evaluation_criteria", []) or []
    ev = module.get("required_evidence", []) or []
    title = module.get("title", "this control area")

    qs = []
    # Use evidence names if present, else criteria
    seeds = ev if ev else crit

    # Keep it bounded
    seeds = seeds[:8] if seeds else [title]

    for item in seeds:
        qs.extend([
            f"Does the organization have documented {item}?",
            f"Who owns and approves {item} (role/title), and when was it last approved?",
            f"How is {item} implemented in day-to-day operations (process + tooling)?",
            f"What evidence demonstrates {item} is operating effectively?",
            f"How often is {item} reviewed/updated, and what triggers an update?",
        ])

    # de-dupe
    dedup = []
    seen = set()
    for q in qs:
        k = q.lower()
        if k not in seen:
            dedup.append(q)
            seen.add(k)

    return dedup[:25]  # cap per module


class QuestionExtractor:
    """Extract questions from text using configurable profiles."""
    
    def __init__(self, config_path: str = "tools/extract_profiles.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.default = self.config.get("default", {})
        
        # Compile common patterns
        self.q_prefix = re.compile(r"^\s*(Q(?:uestion)?\s*\d+(\.\d+)*[:.)-]?)\s+", re.IGNORECASE)
        self.numbered = re.compile(r"^\s*(\d+(\.\d+)*[.)-])\s+")
        self.header = re.compile(r"^\s*[A-Z][A-Z /&-]{4,}\s*$")
        
    def get_profile(self, module_name: str = None) -> Dict[str, Any]:
        """Get extraction profile for a module, falling back to default."""
        if module_name and module_name in self.config:
            # Merge module-specific with defaults
            profile = dict(self.default)
            profile.update(self.config[module_name])
            return profile
        return self.default
    
    def looks_like_question(self, line: str, profile: Dict[str, Any]) -> bool:
        """Check if a line looks like a question based on profile rules."""
        s = line.strip()
        
        # Check min length
        min_len = profile.get("min_question_length", 10)
        if len(s) < min_len:
            return False
        
        # Check max length
        max_len = profile.get("max_question_length", 500)
        if len(s) > max_len:
            return False
        
        # Check skip patterns
        skip_patterns = profile.get("skip_patterns", [])
        for pattern in skip_patterns:
            if re.match(pattern, s):
                return False
        
        # Apply acceptance rules
        accept_rules = profile.get("accept_line_if", [])
        
        for rule in accept_rules:
            if rule == "ends_with_question_mark":
                if s.endswith("?"):
                    return True
            
            elif rule == "starts_with_q_prefix":
                if self.q_prefix.match(s):
                    return True
            
            elif rule == "numbered_question":
                # Numbered prompts that contain question words
                if self.numbered.match(s) and re.search(
                    r"\b(does|do|is|are|should|can|has|have|who|what|when|where|how|will|would|could)\b",
                    s.lower()
                ):
                    return True
        
        return False
    
    def extract_questions(self, lines: List[str], module_name: str = None) -> List[str]:
        """Extract questions from lines using the appropriate profile."""
        profile = self.get_profile(module_name)
        questions = []
        in_q_section = False
        
        # Normalize headers for comparison
        section_headers = [h.lower().rstrip(":") for h in profile.get("question_headers", [])]
        
        # Phase 1: Look for questions in explicit sections
        for line in lines:
            s = line.strip()
            if not s:
                continue
            
            # Check if we're entering a question section
            if s.lower().rstrip(":") in section_headers:
                in_q_section = True
                continue
            
            # Stop if we hit a new obvious header (heuristic)
            if in_q_section and self.header.match(s):
                if s.lower().rstrip(":") not in section_headers:
                    in_q_section = False
            
            # Extract questions from within section
            if in_q_section and self.looks_like_question(s, profile):
                questions.append(s)
        
        # Phase 2: If no section-based questions found, harvest globally
        if not questions:
            questions = [
                ln.strip() 
                for ln in lines 
                if self.looks_like_question(ln, profile)
            ]
        
        # Phase 3: Deduplicate while preserving order
        return self._deduplicate(questions)
    
    def _deduplicate(self, questions: List[str]) -> List[str]:
        """Remove duplicate questions while preserving order."""
        seen = set()
        result = []
        
        for q in questions:
            # Normalize for comparison
            key = re.sub(r"\s+", " ", q.lower().strip())
            if key not in seen:
                result.append(q)
                seen.add(key)
        
        return result


def extract_questions_from_lines(lines: List[str], module_name: str = None) -> List[str]:
    """
    Convenience function for backward compatibility.
    
    Args:
        lines: List of text lines from PDF
        module_name: Optional module name for profile selection
    
    Returns:
        List of extracted question strings
    """
    extractor = QuestionExtractor()
    return extractor.extract_questions(lines, module_name)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_questions.py <text_file> [module_name]")
        sys.exit(1)
    
    text_file = sys.argv[1]
    module_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    with open(text_file) as f:
        lines = f.readlines()
    
    extractor = QuestionExtractor()
    questions = extractor.extract_questions(lines, module_name)
    
    print(f"Extracted {len(questions)} questions:\n")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
