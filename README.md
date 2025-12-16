
# xdfgui

Simple Python GUI wrapper around `xdftool` (from `amitools`) for managing Amiga ADF/HDF images.

Quick Start
-----------

1. Install `uv` (https://docs.astral.sh/uv/) or ensure you have Python 3.11+.
2. From the project root create the virtual environment and install deps:

```bash
cd /path/to/xdfgui
uv venv --python 3.11
source .venv/bin/activate
uv pip sync requirements.txt
```

3. Launch the GUI:

```bash
uv run xdfgui
```

Or run directly:

```bash
uv run python gui.py
```

What this does
--------------

- Creates and formats blank ADF/HDF images
- Lists and shows image contents (parsed into columns)
- Extracts files from images and writes host files into images
- Rename/move/delete files inside images (rename implemented via read->write->delete)
- Split large `.lha` archives into parts and create one ADF per part for distribution across multiple disks

GUI Walkthrough
---------------

- Open Image: choose an existing `.adf` or `.hdf` file to work on. The contents are displayed in a table.
- Create Blank ADF: choose a path to create an empty ADF image file.
- Format ADF: formats the opened image with a volume name and optional DOS type.
- Split LHA -> ADFs: select a `.lha` file and an output directory, choose part size (default near typical ADF capacity). The tool will create ADFs, format them and write each part to a separate ADF.
- Add File: copy a host file into the currently opened image (specify target Amiga path).
- Extract File: extract a chosen Amiga path to a host directory.
- Delete: removes a file or (with confirmation) a directory from the image.
- Rename/Move: rename or move a file within the image (implemented via a temporary extract and write).
- Context menu: right-click any row in the file table to Extract, Delete or Rename the selected item.

CLI Usage
---------

The project exposes a small scripting surface via `xdftool` and the `XdfTool` wrapper.

- Quick create + format (example):

```bash
uv run python -c "from xdfgui.xdftool_wrapper import XdfTool; xd = XdfTool(); xd.create('blank.adf'); xd.format('blank.adf','MyDisk')"
```

- Use `xdftool` directly for advanced operations (the GUI shells out to `xdftool`):

```bash
uv run xdftool mydisk.adf list
uv run xdftool mydisk.adf read c/startup-sequence .
```

Development & Tests
-------------------

- Run unit tests:

```bash
uv run pytest
```

- Tests cover the LHA split/join utilities and the `xdftool list` output parser.

Running on macOS
-----------------

The application includes native macOS integration:
- **Menu bar** with File, Edit, and Tools menus
- **Keyboard shortcuts**: ⌘O (Open), ⌘N (New), ⌘F (Format), ⌘W (Close), ⌘Q (Quit), ⌘A (Add), ⌘E (Extract), ⌘D (Delete), ⌘R (Rename), ⌘L (Refresh)

To run:

```bash
uv sync --extra runtime
uv run xdfgui
```

The app will launch with proper macOS menu integration.

Building macOS Application (Optional)
--------------------------------------

To create a standalone `.app` bundle, you'll need Xcode Command Line Tools:

```bash
xcode-select --install
```

Then install PyInstaller and build:

```bash
uv sync --extra build --extra runtime
uv run pyinstaller xdfgui.spec
```

The application will be created in `dist/xdfgui.app`. You can then run:

```bash
open dist/xdfgui.app
```

Or drag `xdfgui.app` to your Applications folder.

Troubleshooting
---------------

- If `xdftool` is not found, install `amitools` in the environment:

```bash
uv add amitools lhafile
```

- If UI actions hang, ensure the virtual environment's Python is used and `xdftool` is available; the GUI runs long operations in background threads and shows a progress indicator.

Notes
-----

- The GUI uses a permissive parser to convert `xdftool list` textual output into structured columns (Name, Size, Flags, Date, Comment). If you find edge cases, add sample output to `tests/` so the parser can be improved.
- Rename/move is implemented as a read->write->delete because `xdftool` does not provide a direct rename primitive for all FS types.

License & Contributing
----------------------

Contributions welcome. Open an issue or provide a patch. If you want me to push to a remote repository, provide the remote URL.

