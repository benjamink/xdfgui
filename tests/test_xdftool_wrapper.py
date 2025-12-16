import subprocess
from unittest.mock import patch, MagicMock
from xdfgui.xdftool_wrapper import XdfTool


def make_proc(stdout=b"ok", stderr=b"", returncode=0):
    m = MagicMock()
    m.stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
    m.stderr = stderr.decode() if isinstance(stderr, bytes) else stderr
    m.returncode = returncode
    return m


@patch("subprocess.run")
def test_list_and_info(mock_run):
    mock_run.return_value = make_proc(stdout=b"file1\nfile2\n")
    xd = XdfTool(xdftool_cmd="xdftool")
    code, out, err = xd.list("my.adf")
    assert out is not None
    mock_run.assert_called()


@patch("subprocess.run")
def test_create_format_write_delete(mock_run):
    mock_run.return_value = make_proc()
    xd = XdfTool()
    xd.create("a.adf")
    xd.format("a.adf", "VOL")
    xd.write("a.adf", "hostfile.txt")
    xd.read("a.adf", "somefile", "dest")
    xd.delete("a.adf", "somefile")
    assert mock_run.call_count >= 5
