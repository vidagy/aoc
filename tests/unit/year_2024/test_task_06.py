from aoc.util.reader import tokenize_by_char
from aoc.year_2024.task_06 import Guard, get_loops

INP = """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
"""


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n") if line.strip()]


def test_task_06():
    guard = Guard.from_lines(tokenize_by_char(get_lines(INP)))
    assert guard.walk().num_visited() == 41


def test_task_06_p_2():
    lines = tokenize_by_char(get_lines(INP))
    guard = Guard.from_lines(lines)
    guard.walk()
    assert get_loops(guard, lines) == {(6, 3), (7, 6), (7, 7), (8, 1), (8, 3), (9, 7)}
