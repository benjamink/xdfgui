from xdfgui.xdftool_wrapper import XdfTool


def test_parse_simple_line():
    s = "myfile    1024  rwe  06.07.1986 14:38:56  some comment"
    parsed = XdfTool().parse_list_output(s)
    assert len(parsed) == 1
    p = parsed[0]
    assert p["name"] == "myfile"
    assert p["size"] == "1024"
    assert p["flags"] == "rwe"
    assert "06.07.1986" in p["date"]
    assert "some comment" in p["comment"]


def test_parse_name_with_spaces_and_no_size():
    s = "Long Name    r--    06.07.1990  comment only"
    parsed = XdfTool().parse_list_output(s)
    assert parsed[0]["name"] == "Long Name"
    assert parsed[0]["flags"] == "r--"


def test_parse_comma_size_and_suffix():
    s = "bigfile    1,024K    rwe  01.01.2000  note"
    parsed = XdfTool().parse_list_output(s)
    assert parsed[0]["size"] == "1,024K"
