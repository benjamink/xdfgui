#!/usr/bin/env bash
# Minimal helper to create uv venv and install deps
set -euo pipefail
echo "Creating uv virtual environment and installing dependencies..."
uv venv --python 3.11
echo "Activate with: source .venv/bin/activate"
echo "Installing packages from requirements.txt"
uv pip sync requirements.txt
echo "Done. Run 'uv run python gui.py' to start the GUI"
