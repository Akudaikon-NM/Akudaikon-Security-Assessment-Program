# Codespace Setup Guide

## ✅ Current Repository Structure

Your repository is already properly structured for Codespaces:

```
/workspaces/Akudaikon-Security-Assessment-Program/
├── apps/
│   └── assessor_streamlit/          # Streamlit application
│       ├── app.py                   # Main app entry point
│       ├── scoring.py
│       ├── findings.py
│       ├── reporting.py
│       └── module_loader.py
├── control_library/
│   └── modules/                     # 25+ YAML control modules
│       ├── 01_policies_and_procedures.yaml
│       ├── 02_governance.yaml
│       └── ... (23+ more modules)
├── core/                            # Core business logic
├── outputs/                         # Generated reports
├── requirements.txt                 # Python dependencies
└── .devcontainer/                   # Codespace configuration
    └── devcontainer.json
```

## 🚀 Quick Start in Codespaces

### Option 1: Using VS Code Tasks (Recommended)
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select "Run Streamlit App"

### Option 2: Using Terminal
```bash
streamlit run apps/assessor_streamlit/app.py
```

### Option 3: Manual with Full Options
```bash
python -m streamlit run apps/assessor_streamlit/app.py \
  --server.headless=true \
  --server.port=8501 \
  --server.address=0.0.0.0
```

## 🔌 Port Configuration

Streamlit runs on **port 8501** by default. Codespaces automatically:
- Detects the port when the app starts
- Forwards it to your local browser
- Shows a notification with the URL to click

### Verify Port Forwarding
1. Look for the "Ports" tab in VS Code (bottom panel)
2. Confirm port 8501 is listed and forwarded
3. Click the globe icon or local address to open the app

### Manual Port Check
```bash
ss -tlnp | grep 8501
```

## 📦 Dependencies

All required packages are in `requirements.txt`:
- `streamlit` - Web UI framework
- `fastapi` - API framework (for future use)
- `uvicorn` - ASGI server
- `pyyaml` - YAML parsing
- `pydantic` - Data validation

### Install/Reinstall Dependencies
```bash
pip install -r requirements.txt
```

## 📂 Directory Structure Notes

**Your structure is CORRECT and follows best practices:**

❌ **Don't restructure** to a flat layout - your current multi-tier structure is superior:
- Separates concerns (apps vs core vs control library)
- Allows multiple apps to share the control library
- Easier to maintain and scale

✅ **Keep your current structure** with:
- Apps in `apps/` directory
- Control library in `control_library/modules/`
- Core logic in `core/`
- Outputs in `outputs/`

## 🎯 Module Loader Path Resolution

The `module_loader.py` correctly resolves paths:
```python
BASE_PATH = Path(__file__).resolve().parents[2] / "control_library" / "modules"
```

This works from `apps/assessor_streamlit/module_loader.py`:
- `parents[0]` → `apps/assessor_streamlit/`
- `parents[1]` → `apps/`
- `parents[2]` → repository root
- Then navigates to `control_library/modules/`

**No changes needed!**

## 🛠️ Troubleshooting

### App won't start
```bash
# Check Python version (should be 3.12+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with verbose output
streamlit run apps/assessor_streamlit/app.py --logger.level=debug
```

### Port not forwarding
1. Check the Ports tab in VS Code
2. Manually forward port 8501 if needed:
   - Ports tab → Forward a Port → 8501
3. Or use `--server.address=0.0.0.0` flag

### Module not found errors
```bash
# Verify you're in the repository root
pwd
# Should show: /workspaces/Akudaikon-Security-Assessment-Program

# Verify control library exists
ls -la control_library/modules/
```

## 🎓 Learning Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Codespaces Docs](https://docs.github.com/en/codespaces)
- [Dev Container Spec](https://containers.dev/)

## 📝 Next Steps

1. ✅ Environment configured
2. ✅ Dependencies installed
3. ✅ App running on port 8501
4. ✅ Port forwarding enabled
5. 👉 **Open the app and start assessing!**

Access your running app at the URL shown in the terminal or Ports tab.
