from aoc.util.reader import convert, split_lines_by_empty_line, tokenize_by_char


def test_split_lines_by_empty_line():
    inp = ["asd", "bds", "", "csd"]
    res = split_lines_by_empty_line(inp)
    assert res == [["asd", "bds"], ["csd"]]


def test_split_lines_by_empty_line_2():
    inp = ["asd", "bds", "", "", "csd"]
    res = split_lines_by_empty_line(inp)
    assert res == [["asd", "bds"], ["csd"]]


def test_tokenize_by_char():
    inp = ["123", "456", "789"]
    res = tokenize_by_char(inp)
    assert res == [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]


INPUT = """
199
200
208

200
207
240
"""


def test_input():
    inp = INPUT.split("\n")
    maps = [convert(tokenize_by_char(m), int) for m in split_lines_by_empty_line(inp)]

    assert maps == [
        [[1, 9, 9], [2, 0, 0], [2, 0, 8]],
        [[2, 0, 0], [2, 0, 7], [2, 4, 0]],
    ]
