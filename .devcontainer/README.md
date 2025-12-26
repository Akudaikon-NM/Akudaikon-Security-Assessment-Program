# Devcontainer Configuration

This devcontainer is configured for the Akudaikon Security Assessment Program.

## Features

- **Python 3.12** environment
- **Auto port forwarding** for Streamlit (8501) and FastAPI (8000)
- **Auto-install dependencies** on container creation
- **Pre-configured VS Code extensions** for Python and YAML development

## Quick Start

1. Open this repository in GitHub Codespaces or VS Code with Dev Containers extension
2. Wait for the container to build and dependencies to install
3. Run the Streamlit app:
   ```bash
   streamlit run apps/assessor_streamlit/app.py
   ```
4. Access the app via the forwarded port notification

## Manual Setup (if needed)

If you need to manually install dependencies:
```bash
pip install -r requirements.txt
```

## Port Forwarding

- **Port 8501**: Streamlit assessment application
- **Port 8000**: FastAPI backend (when used)

Ports are automatically forwarded in Codespaces and Dev Containers.
