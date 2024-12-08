from aoc.year_2024.task_08 import Field


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n") if line.strip()]


INP = """
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
"""


def test_task_08_resonants():
    field = Field(get_lines(INP))

    assert field.get_antinodes(field.antennas["T"], resonants=True) == {
        (0, 0),
        (0, 5),
        (1, 3),
        (2, 1),
        (2, 6),
        (3, 9),
        (4, 2),
        (6, 3),
        (8, 4),
    }
