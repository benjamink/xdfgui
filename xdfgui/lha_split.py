from pathlib import Path
import math


DEFAULT_ADF_CAPACITY = 901120  # bytes (typical ADF size)


def split_file(path: str, part_size: int = None, out_dir: str = None):
    p = Path(path)
    if part_size is None:
        part_size = DEFAULT_ADF_CAPACITY - 20000  # reserve some overhead
    if out_dir is None:
        out_dir = str(p.parent)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    file_size = p.stat().st_size
    parts = math.ceil(file_size / part_size)
    out_paths = []
    with p.open("rb") as fh:
        for i in range(parts):
            chunk = fh.read(part_size)
            part_name = f"{p.stem}.part{i+1:02d}{p.suffix}"
            out_path = out_dir / part_name
            with out_path.open("wb") as of:
                of.write(chunk)
            out_paths.append(str(out_path))
    return out_paths


def join_parts(part_paths, out_path: str):
    outp = Path(out_path)
    with outp.open("wb") as of:
        for p in part_paths:
            with Path(p).open("rb") as fh:
                shutil = fh.read()
                of.write(shutil)
    return str(outp)
