# Demo Guide - Akudaikon Security Assessment

## 🚀 Quick Start

### Access the Application

**Streamlit is running on port 8501**

1. Look for the **"PORTS"** tab at the bottom of VS Code
2. Find port **8501**
3. Click the **🌐 globe icon** to open in browser

## 📝 Demo Scenario

### Module Information

⚠️ **Important:** Use `13_access_controls` not `01_access_control`

- **Module:** 13_access_controls — 13 Access Controls
- **Questions:** 5 assessment questions
- **Mode:** Assessor mode

### Step-by-Step Demo

#### 1. Select Module
From the dropdown at the top:
```
Select Module: 13_access_controls — 13 Access Controls
```

#### 2. Choose Mode
In the left sidebar:
```
Mode: Assessor mode
```

#### 3. Fill Out Client Information (Optional)
In the sidebar:
- Institution name: (your choice)
- Assets: (optional)
- Primary regulator: NCUA
- Hosting model: Customer-hosted

#### 4. Answer Assessment Questions

The module has 5 questions. For demo purposes, use this pattern:

| Question | Demo Answer |
|----------|-------------|
| Q1: Does the organization have documented 13 Access Controls? | **Yes** |
| Q2: Who owns and approves 13 Access Controls (role/title), and when was it last approved? | **No** |
| Q3: How is 13 Access Controls implemented in day-to-day operations (process + tooling)? | **Partial** |
| Q4: What evidence demonstrates 13 Access Controls is operating effectively? | **Yes** |
| Q5: How often is 13 Access Controls reviewed/updated, and what triggers an update? | **Partial** |

#### 5. Generate Assessment
- Scroll to the bottom
- Click the **"Assess"** button
- Wait for the report to generate

### Expected Output

The app will generate:

✅ **Scorecard**
- Overall compliance rating (Pass/Partial/Fail)
- Breakdown by control area

✅ **Findings**
- Examiner-grade findings with regulatory citations
- Deterministic based on your answers

✅ **Evidence Analysis**
- Requested evidence vs. provided
- Gap identification

✅ **Remediation Plan**
- Targeted recommendations
- Priority levels

✅ **Board Report**
- Executive summary
- Risk implications
- ROI considerations

## 📊 Other Modules to Try

After completing the demo with Access Controls, try these modules:

1. **01_policies_and_procedures** — Policies & Procedures
2. **02_governance** — Governance
3. **04_risk_assessment** — Risk Assessment
4. **08_incident_response** — Incident Response
5. **14_network_security** — Network Security

**Total available modules: 39**

All follow the same workflow!

## 🎯 Key Features to Demonstrate

### Intake Mode
- Collect evidence and answers
- Track documentation
- Export responses

### Assessor Mode
- Generate compliance scores
- Create examiner-grade findings
- Produce board-ready reports

## 🔄 Troubleshooting

### App Not Loading?
```bash
# Restart Streamlit
pkill -f streamlit
cd apps/assessor_streamlit
streamlit run app.py
```

### Port Not Visible?
1. Check the **PORTS** tab in VS Code
2. Manually forward port 8501 if needed
3. Or use the VS Code task: `Ctrl+Shift+P` → "Run Streamlit App"

### Module Not Found?
- Make sure you selected `13_access_controls` (not `01_access_control`)
- The dropdown shows all 39 available modules

## 📚 Application Features

### Two Operating Modes

**Intake Mode:**
- Evidence collection interface
- Question-by-question workflow
- Notes and documentation tracking

**Assessor Mode:**
- Quick assessment entry
- Overall compliance selection
- Instant report generation

### Regulatory Alignment

All assessments are aligned to:
- **GLBA 501(b)** - Safeguards Rule
- **12 CFR 748.0** - Security Program requirements
- **12 CFR 748.1** - Certification & Reporting
- **Appendix A/B** - Implementation guidance

## 🎓 What This Demonstrates

1. **Evidence-led assessment** - Anchored to regulatory requirements
2. **Deterministic findings** - Based on YAML logic, not AI
3. **Examiner-grade output** - Professional compliance reporting
4. **Scalable framework** - 39 modules covering comprehensive controls
5. **Board-ready reports** - Executive-level summaries

## ✅ Success Criteria

After completing the demo, you should have:
- [x] Accessed the Streamlit application
- [x] Selected a control module
- [x] Answered assessment questions
- [x] Generated a compliance report
- [x] Viewed findings and recommendations

---

**Your demo environment is ready!** Open port 8501 in your browser to begin.
