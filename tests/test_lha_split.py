import tempfile
from pathlib import Path
from xdfgui.lha_split import split_file, join_parts


def test_split_and_join(tmp_path):
    data = b"A" * 10000 + b"B" * 5000 + b"C" * 3000
    src = tmp_path / "test.lha"
    src.write_bytes(data)

    parts = split_file(str(src), part_size=7000, out_dir=str(tmp_path))
    assert len(parts) >= 3

    joined = tmp_path / "joined.lha"
    join_parts(parts, str(joined))
    assert joined.read_bytes() == data
