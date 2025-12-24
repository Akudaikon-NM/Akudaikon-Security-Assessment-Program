import streamlit as st
from module_loader import list_modules, load_module
from scoring import generate_scorecard
from findings import generate_findings
from reporting import generate_report

st.title("Akudaikon | 748/GLBA Assessor")
st.write("Welcome to the security assessment tool.")

modules = list_modules()  # returns (filename_stem, title)

# Use a stable label so titles can't collide
module_options = {f"{stem} — {title}": stem for stem, title in modules}
selected_label = st.selectbox("Select Module", list(module_options.keys()))

if not selected_label:
    st.stop()

module_stem = module_options[selected_label]
module_data = load_module(module_stem) or {}

st.write("**Evaluation Criteria:**")
for crit in module_data.get('evaluation_criteria', []):
    st.write(f"- {crit}")

st.write("**Required Evidence:")
for ev in module_data.get('required_evidence', []):
    st.write(f"- {ev}")

overall = st.selectbox("Overall Compliance", ['full', 'partial', 'none'], key='overall')

if st.button("Assess"):
    scorecard = generate_scorecard(module_data, {'overall': overall})
    findings = generate_findings(module_data, scorecard)
    report = generate_report(scorecard, findings)
    st.text_area("Report", report, height=300)