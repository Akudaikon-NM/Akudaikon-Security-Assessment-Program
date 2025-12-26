import streamlit as st
from module_loader import list_modules, load_module
from scoring import generate_scorecard
from findings import generate_findings
from reporting import generate_report

st.set_page_config(page_title="Akudaikon | 748/GLBA Assessor", layout="wide")
st.title("Akudaikon | 748/GLBA Assessor")
st.caption("Evidence-led control assessment aligned to GLBA and 12 CFR Part 748.")

# ---------- helpers ----------
def q_prompt(q):
    if isinstance(q, dict):
        return q.get("prompt") or q.get("question") or ""
    return str(q)

def q_reference(q):
    return q.get("reference", "") if isinstance(q, dict) else ""

def q_evidence_requests(q):
    return q.get("evidence_requests", []) if isinstance(q, dict) else []

def q_id(q, fallback):
    if isinstance(q, dict):
        return q.get("id") or q.get("qid") or fallback
    return fallback


# ---------- sidebar: global controls ----------
with st.sidebar:
    st.header("Mode")
    mode = st.radio("Select workflow", ["Intake mode", "Assessor mode"], index=0)

    st.divider()
    st.header("Client Intake")
    st.text_input("Institution name", key="inst_name")
    st.text_input("Assets (optional)", key="assets")
    st.selectbox("Primary regulator", ["NCUA", "State", "Dual"], index=0, key="regulator")
    st.radio("Hosting model", ["Customer-hosted", "Consultant-hosted"], index=0, key="hosting")


# ---------- module selection ----------
modules = list_modules()
if not modules:
    st.error("No modules found. Check control_library/modules.")
    st.stop()

module_options = {f"{stem} — {title}": stem for stem, title in modules}
selected_label = st.selectbox("Select Module", list(module_options.keys()))
module_stem = module_options[selected_label]
module = load_module(module_stem) or {}

if module.get("__warnings__"):
    st.warning("Module missing keys: " + ", ".join(module["__warnings__"]))
    st.caption(f"Loaded from: {module.get('__file__')}")

st.subheader(module.get("title", "Untitled Module"))
if module.get("description"):
    st.write(module["description"])
st.write(module.get("control_objective", "⚠️ control_objective missing in YAML"))

st.markdown("### Evaluation Criteria")
for crit in module.get("evaluation_criteria", []):
    st.write(f"- {crit}")

st.markdown("### Required Evidence")
for ev in module.get("required_evidence", []):
    st.write(f"- {ev}")

questions = module.get("questions", [])


# ---------- INTAKE MODE ----------
def render_intake_mode():
    st.divider()
    tabs = st.tabs(["Questions", "Evidence Requests", "Findings & Remediation", "Export"])

    with tabs[0]:
        st.markdown("## Questions")
        src = (module.get("__meta__", {}) or {}).get("questions_source", "unknown")
        st.caption(f"Questions source: {src}")
        if not questions:
            st.info("No questions found for this module.")
            return

        for i, q in enumerate(questions, start=1):
            qtext = q_prompt(q)
            qref = q_reference(q)
            qkey = f"{module.get('module_id','mod')}_{q_id(q,f'q{i}')}"
            st.markdown(f"**Q{i}. {qtext}**")
            if qref:
                st.caption(f"Reference: {qref}")
            st.radio("Response", ["Yes", "No", "Partial", "N/A"], horizontal=True, key=f"{qkey}_resp")
            st.text_area("Notes / evidence summary", height=80, key=f"{qkey}_notes")
            st.markdown("---")

    with tabs[1]:
        st.markdown("## Evidence Requests")
        if not questions:
            st.info("No questions found for this module.")
            return

        for i, q in enumerate(questions, start=1):
            qtext = q_prompt(q)
            evs = q_evidence_requests(q)
            qkey = f"{module.get('module_id','mod')}_{q_id(q,f'q{i}')}"
            st.markdown(f"**Evidence for Q{i}: {qtext}**")
            if evs:
                for ev in evs:
                    st.write(f"- {ev}")
            else:
                st.caption("No evidence_requests listed for this question.")
            st.file_uploader("Upload files (v1 stub)", accept_multiple_files=True, key=f"{qkey}_uploads")
            st.markdown("---")

    with tabs[2]:
        st.markdown("## Findings & Remediation (starter)")
        fps = module.get("finding_patterns", [])
        if not fps:
            st.caption("No finding_patterns in YAML yet.")
        for f in fps:
            st.markdown(f"- **{f.get('type','').title()}**: {f.get('text','')}")
            if f.get("remediation"):
                st.caption("Remediation starter:")
                for r in f["remediation"]:
                    st.write(f"  - {r}")

    with tabs[3]:
        st.markdown("## Export (stub)")
        st.info("Next: generate board-ready summary + evidence index + remediation plan files under /outputs.")
        st.button("Generate report (stub)")
        st.button("Generate remediation plan (stub)")


# ---------- ASSESSOR MODE ----------
def render_assessor_mode():
    st.divider()
    st.markdown("## Assessor Mode (scoring + report)")

    if not questions:
        st.info("No questions found. Add `questions:` in YAML to enable scoring.")
        overall = st.selectbox("Overall Compliance", ["full", "partial", "none"])
        if st.button("Assess"):
            scorecard = generate_scorecard(module, {"overall": overall})
            findings = generate_findings(module, scorecard)
            report = generate_report(scorecard, findings)
            st.text_area("Report", report, height=400)
        return

    responses[qid] = {
    "response": selected_value,      # "Yes" / "Partial" / "No" / "N/A"
    "explanation": explanation_text, # optional
    "evidence": evidence_text,       # optional
}


    with st.form(key=f"assess_form_{module_stem}"):
        for i, q in enumerate(questions, start=1):
            qtext = q_prompt(q)
            qkey = q_id(q, f"q{i}")

            st.markdown(f"**{i}. {qtext}**")
            resp = st.radio("Response", ["Yes", "Partial", "No", "N/A"], horizontal=True, key=f"{module_stem}_{qkey}_resp2")
            note = st.text_area("Notes / Evidence reference (optional)", height=80, key=f"{module_stem}_{qkey}_note2")

            responses[qkey] = {"question": qtext, "response": resp}
            notes[qkey] = note
            st.markdown("---")

        submitted = st.form_submit_button("Assess")

    if submitted:
    # Ensure every response entry is in the {"response": "..."} dict format
    normalized_responses = {}
    for qid, item in (responses or {}).items():
        if isinstance(item, dict):
            # If your UI stored the response under some other key, map it here:
            if "response" not in item and "answer" in item:
                item["response"] = item.get("answer")
            normalized_responses[qid] = item
        else:
            # If the UI stored a raw string, wrap it
            normalized_responses[qid] = {"response": item}

    assessment_input = {
        "responses": normalized_responses,
        "notes": notes,
    }

    scorecard = generate_scorecard(module, assessment_input)

    # ... rest of your code


        st.success("Assessment generated.")
        st.text_area("Assessment Report", report, height=450)

        with st.expander("Scorecard (debug)"):
            st.json(scorecard)
        with st.expander("Findings (debug)"):
            st.json(findings)


# ---------- switch ----------
if mode == "Intake mode":
    render_intake_mode()
else:
    render_assessor_mode()
