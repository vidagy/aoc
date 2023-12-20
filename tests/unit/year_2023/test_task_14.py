import pytest

from aoc.year_2023.task_14 import Direction, Platform

INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".split()

OUTPUT_NORTH = """
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
"""


def test_north():
    p = Platform(INPUT)
    p.tilt(Direction.NORTH)

    assert OUTPUT_NORTH == str(p)
    assert p.get_weight(Direction.NORTH) == 136


OUTPUT_1 = """
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
"""

OUTPUT_2 = """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
"""

OUTPUT_3 = """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
"""


@pytest.mark.parametrize(
    "num_cycle, expected_output", [(1, OUTPUT_1), (2, OUTPUT_2), (3, OUTPUT_3)]
)
def test_1_cycle(num_cycle, expected_output):
    p = Platform(INPUT)
    for i in range(num_cycle):
        for d in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]:
            p.tilt(d)
    assert expected_output == str(p)
