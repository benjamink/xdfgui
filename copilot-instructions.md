# Copilot instructions for this repository

This document explains repository conventions and guidance for an assistant working on this project.

- Project layout:
  - `gui.py` — top-level GUI runner (Tkinter).
  - `xdfgui/` — package containing modules:
    - `xdftool_wrapper.py` — shell wrapper and parser for `xdftool`.
    - `lha_split.py` — utilities to split/join large `.lha` files.
    - `cli.py` — entry point that launches the GUI.
  - `tests/` — pytest-based tests.
  - `requirements.txt` and `pyproject.toml` — dependency hints and packaging metadata.

- Environment and tooling:
  - The project uses `uv` for environment management; a `.python-version` pins Python 3.11.
  - Use the virtual environment at `.venv` created by `uv venv` for running and testing.
  - Tests run with `pytest` (invoke via `.venv/bin/python -m pytest` or `uv run pytest`).

- Development & edits:
  - Use `apply_patch` when editing repository files (keep edits minimal and focused).
  - Run unit tests after changes and fix any introduced failures before committing.
  - Keep changes backwards-compatible unless the user requests breaking changes.
  - Follow the project's coding style: simple, readable Python; avoid unnecessary comments.
  - Do not add license headers unless explicitly requested.

- Commit & project scripts:
  - Commits should be small and descriptive. Use existing commit message style.
  - The package exposes a console script `xdfgui` (declared in `pyproject.toml`).

- GUI behavior expectations:
  - Long-running operations must not block the UI — run them in background threads and provide a status/progress indicator.
  - Use `xdftool` for disk operations; parse `xdftool list` output into structured rows for display.
  - For operations lacking a direct xdftool command (rename/move), use extract/write/delete as implemented.

- When referencing files or symbols in messages, wrap filenames in backticks (e.g. `gui.py`).

- Tests and examples:
  - Place unit tests in `tests/` using `pytest`.
  - Include small, deterministic tests for parsing `xdftool` output and the LHA split/join utilities.

If you need remote push access, ask the user for a remote URL before pushing.
