# Control Library Modules

This directory contains the assessment modules for the Akudaikon 748 Assessor.

## Module Structure

Each module YAML file follows the schema defined in `schema.yaml`.

Modules are numbered for ordering and include:

- module_id: Unique identifier
- title: Human-readable title
- primary_requirements: Enforceable GLBA/§748 citations
- guidance_alignment: Former Appendix A/B references
- control_objective: What must exist
- evaluation_criteria: How adequacy is determined
- required_evidence: Evidence needed for assessment
- finding_templates: Positive/partial/negative examiner-style findings

## Available Modules

| ID | Module | Regulatory Focus |
|----|--------|------------------|
| 01 | Policies and Procedures | GLBA Safeguards Rule, 12 CFR §748.1(c) |
| 02 | Governance and Board Oversight | GLBA §501(b), 12 CFR §748.0(b)(2) |
| 03 | Asset Inventory | GLBA Safeguards Rule |
| 04 | Risk Assessment | GLBA Safeguards Rule |
| 05 | Controls Testing | GLBA Safeguards Rule |
| 06 | Corrective Actions | GLBA Safeguards Rule |
| 07 | Training | GLBA Safeguards Rule |
| 08 | Incident Response | GLBA Safeguards Rule |
| 09 | Third Party Risk Management | GLBA Safeguards Rule |
| 10 | Business Continuity/Disaster Recovery | GLBA Safeguards Rule |
| 11 | Vulnerability and Patch Management | GLBA Safeguards Rule |
| 12 | Antivirus and Antimalware Controls | GLBA Safeguards Rule |
| 13 | Access Controls | GLBA Safeguards Rule |
| 14 | Network Security | GLBA Safeguards Rule |
| 15 | Data Leak Protection | GLBA Safeguards Rule |
| 16 | Change and Configuration Management | GLBA Safeguards Rule |
| 17 | Monitoring | GLBA Safeguards Rule |
| 18 | Logging and Monitoring Activities | GLBA Safeguards Rule |
| 19 | Data Governance | GLBA Safeguards Rule |
| 20 | Core Conversion Management | GLBA Safeguards Rule |
| 21 | Software Development Process | GLBA Safeguards Rule |
| 22 | Internal Audit Program | GLBA §501(b), 12 CFR §748 |
| 23 | AI Review | Model risk, governance |
| 24 | Security Controls Questionnaire | Control coverage |
| 25 | CIS Controls ROI Library | Risk reduction economics |

## Authoring Guidelines

- Anchor findings to primary_requirements, not guidance
- Use examiner-style language in finding_templates
- Keep evaluation_criteria specific and measurable
- Reference PDFs in docs/source_pdfs/ for detailed guidance