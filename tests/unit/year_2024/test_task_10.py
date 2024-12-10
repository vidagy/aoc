from aoc.util.reader import convert, tokenize_by_char
from aoc.year_2024.task_10 import Point, TopographicMap


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n") if line.strip()]


INP_1 = """
    5550555
    5551555
    5552555
    6543456
    7555557
    8555558
    9555559
"""


def test_task_10_1():
    topo_map = TopographicMap(convert(tokenize_by_char(get_lines(INP_1)), int))

    assert topo_map.get_trails_from(Point(0, 3, 0)) == [
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 4, 4),
            Point(3, 5, 5),
            Point(3, 6, 6),
            Point(4, 6, 7),
            Point(5, 6, 8),
            Point(6, 6, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(3, 1, 5),
            Point(3, 0, 6),
            Point(4, 0, 7),
            Point(5, 0, 8),
            Point(6, 0, 9),
        ],
    ]


INP_2 = """
    5590559
    5551598
    5552557
    6543456
    7655987
    8765555
    9875555
"""


def test_task_10_2():
    topo_map = TopographicMap(convert(tokenize_by_char(get_lines(INP_2)), int))

    assert topo_map.get_trails_from(Point(0, 3, 0)) == [
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 4, 4),
            Point(3, 5, 5),
            Point(3, 6, 6),
            Point(4, 6, 7),
            Point(4, 5, 8),
            Point(4, 4, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 4, 4),
            Point(3, 5, 5),
            Point(3, 6, 6),
            Point(2, 6, 7),
            Point(1, 6, 8),
            Point(0, 6, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 4, 4),
            Point(3, 5, 5),
            Point(3, 6, 6),
            Point(2, 6, 7),
            Point(1, 6, 8),
            Point(1, 5, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(4, 2, 5),
            Point(5, 2, 6),
            Point(6, 2, 7),
            Point(6, 1, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(4, 2, 5),
            Point(5, 2, 6),
            Point(5, 1, 7),
            Point(6, 1, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(4, 2, 5),
            Point(5, 2, 6),
            Point(5, 1, 7),
            Point(5, 0, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(4, 2, 5),
            Point(4, 1, 6),
            Point(5, 1, 7),
            Point(6, 1, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(4, 2, 5),
            Point(4, 1, 6),
            Point(5, 1, 7),
            Point(5, 0, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(4, 2, 5),
            Point(4, 1, 6),
            Point(4, 0, 7),
            Point(5, 0, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(3, 1, 5),
            Point(4, 1, 6),
            Point(5, 1, 7),
            Point(6, 1, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(3, 1, 5),
            Point(4, 1, 6),
            Point(5, 1, 7),
            Point(5, 0, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(3, 1, 5),
            Point(4, 1, 6),
            Point(4, 0, 7),
            Point(5, 0, 8),
            Point(6, 0, 9),
        ],
        [
            Point(0, 3, 0),
            Point(1, 3, 1),
            Point(2, 3, 2),
            Point(3, 3, 3),
            Point(3, 2, 4),
            Point(3, 1, 5),
            Point(3, 0, 6),
            Point(4, 0, 7),
            Point(5, 0, 8),
            Point(6, 0, 9),
        ],
    ]
