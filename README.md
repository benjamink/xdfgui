# xdfgui

Simple Python GUI wrapper around `xdftool` (from `amitools`) to manage ADF/HDF images.

Features:
- Create and format ADF images
- List contents, extract and write files
- Delete/rename/move files inside images (via read/write/delete)
- Split large `.lha` files into parts and put parts onto multiple ADF images

Setup (using `uv`):

1. Install `uv` (see https://docs.astral.sh/uv/)
2. From this project directory run:

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip sync requirements.txt
```

Or simply:

```bash
uv add amitools lhafile
```

Run the GUI:

```bash
uv run python gui.py
```

Notes:
- This tool shells out to the `xdftool` command (installed as part of `amitools`).
- Renaming/moving a file is implemented by copying to host, writing under new name and deleting the old entry.
