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

Example Workflows
-----------------

1) Create and format a blank ADF via CLI

```bash
uv run python -c "from xdfgui.xdftool_wrapper import XdfTool; xd = XdfTool(); xd.create('blank.adf'); xd.format('blank.adf', 'MyDisk')"
```

2) Inspect contents of an ADF via CLI

```bash
uv run xdftool mydisk.adf list
```

3) Using the GUI

- Run `uv run xdfgui` or `uv run python gui.py` to start the app.
- Click `Open Image` to select an existing `.adf`.
- Use `Add File` to copy a host file into the image, `Extract File` to pull files out.
- Use `Split LHA -> ADFs` to split a large `.lha` archive into parts and create one ADF per part.

