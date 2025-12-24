# Akudaikon 748 Assessor

Evidence-led assessment tool for evaluating a credit union’s security program against enforceable regulatory requirements (GLBA 501(b), 12 CFR 748.0 Security Program, and 12 CFR 748.1 Certification + Reporting), with former Appendix A/B content treated as guidance alignment (e.g., Letters to Credit Unions), not "rule text".

The tool produces examiner-grade outputs including scorecards by requirement, evidence indexes, findings with remediation plans, and board-ready reports. Regulatory logic runs headless (CLI/API) and does not depend on Streamlit or an LLM. Streamlit is an optional UI layer.

## Regulatory Basis

### Enforceable Anchors
- **GLBA 501(b)**: Requires financial institutions to implement administrative, technical, and physical safeguards to protect customer information security and confidentiality, against anticipated threats, and against unauthorized access causing substantial harm.
- **12 CFR 748.0 (Security Program)**: Translates GLBA into specific, enforceable program obligations for federally insured credit unions, including written security programs, risk assessments, incident response, and proper disposal of consumer information.
- **12 CFR 748.1 (Certification + Reporting)**: Annual certification of compliance, catastrophic act reporting, cyber incident reporting within 72 hours, and Suspicious Activity Report (SAR) coordination.

### Guidance Alignment
Former Appendix A (Information Security Program Guidelines) and Appendix B (Response Programs and Member Notice Guidance) are treated as interpretive guidance for program governance, risk assessment, incident response, and board reporting. Findings and ratings are anchored to enforceable requirements, not guidance alone.

## What’s in this Repo

- `/control_library/modules/` — Canonical YAML assessment modules (25 modules covering policies through CIS controls).
- `/docs/source_pdfs/` — Canonical PDF sources for reference (policies, appendices, etc.).
- `/apps/assessor_streamlit/` — Lightweight demo UI (Streamlit runner for walkthrough + evidence intake).
- `/outputs/` — Generated artifacts (assessments, board reports, remediation plans, evidence index).

## Quickstart (Demo Runner)

### 1. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
streamlit run apps/assessor_streamlit/app.py
```

### 3. Select Module and Assess
- Choose a module from the dropdown.
- Review control objective, evaluation criteria, and required evidence.
- Select overall compliance level.
- Click "Assess" to generate scorecard, findings, and report.

### 4. Export Report
- Copy the generated text report or integrate with future export features.

## Assessment Workflow (v1)

1. **Select Modules**: Choose from 25 canonical modules based on credit union size/complexity.
2. **Answer Prompts**: Provide compliance levels for evaluation criteria.
3. **Attach Evidence**: Reference required evidence (links to PDFs in `/docs/source_pdfs/`).
4. **Generate Outputs**:
   - Assessment summary with Pass/Partial/Fail by requirement.
   - Evidence index (requested vs. provided evidence + gaps).
   - Findings with examiner-style language + targeted remediation.
   - Board-ready report (highlights + ROI implications).

## Module Authoring Guide (YAML)

Modules are authored in `/control_library/modules/` as YAML files with required keys:

- `module_id`: Unique identifier (e.g., "01_governance").
- `title`: Human-readable title.
- `primary_requirements`: List of enforceable GLBA/§748 citations.
- `guidance_alignment`: List of guidance references (optional).
- `control_objective`: What must exist.
- `evaluation_criteria`: How adequacy is determined.
- `required_evidence`: Evidence needed for assessment.
- `finding_templates`: Positive/partial/negative examiner-style findings.

Scoring rubric: Pass (full compliance), Partial (gaps exist), Fail (significant deficiencies).

Future: Schema validation via `schema.yaml`.

## AI Rewrite Workflow (v1.1)

"Review docs → Summarize gaps → Draft rewrite → Human approval"

- Document ingestion + chunking for policy analysis.
- Map chunks to control/questions for gap identification.
- Generate remediation drafts with citation references.
- **AI is assistive only; all outputs require human approval** to ensure accuracy and compliance.
- Data handling: Documents processed locally; no external transmission without consent.

## Loss Modeling Integration (v1.2)

Link control posture to quantitative risk outputs:

- Map security controls to loss reduction curves.
- Board deliverables: Expected Annual Loss (EAL), Value at Risk (VaR), Conditional VaR (CVaR), and ROI of controls.
- Scenario library: Ransomware, BEC, third-party breaches, operational outages.

## SaaS Roadmap (v2)

- Multi-tenant platform with per-client segregation.
- Evidence vault with retention, legal hold, and chain-of-custody.
- Role-Based Access Control (RBAC) + audit logging.
- API-first architecture + automated assessments/reminders/dashboards.

## Security & Data Handling

- **Document Retention**: Evidence retained per regulatory requirements; customer controls deletion.
- **PII Handling**: No storage of sensitive data; assessments reference metadata only.
- **Customer-Hosted Option**: Preferred for regulated clients to maintain data residency and liability.
- **Chain-of-Custody**: All evidence links traceable; audit trails for compliance.

## License / Disclaimer

This tool is an assessment support tool, not legal advice. Outputs should be reviewed by qualified compliance professionals. Not affiliated with NCUA or any regulatory body.