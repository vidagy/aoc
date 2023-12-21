import logging
from dataclasses import dataclass
from enum import Enum

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class Direction(Enum):
    Up = "U"
    Right = "R"
    Down = "D"
    Left = "L"


StepT = tuple[int, int]

STEP: dict[Direction, StepT] = {
    Direction.Up: (-1, 0),
    Direction.Right: (0, 1),
    Direction.Left: (0, -1),
    Direction.Down: (1, 0),
}


@dataclass
class Edge:
    dir: Direction
    length: int
    color: str

    def __init__(self, line: str) -> None:
        d, l, c = line.split()

        self.dir = Direction(d)
        self.length = int(l)
        self.color = c.strip("()")

    def transform_by_color(self) -> "Edge":
        c = self.color.strip("#")
        m = {
            0: Direction.Right,
            1: Direction.Down,
            2: Direction.Left,
            3: Direction.Up,
        }
        dir = m[int(c[-1])]
        length = int(c[:-1], 16)

        return Edge(f"{dir.value} {length} ({self.color})")


def get_extremes_from_edges(edges: list[Edge]) -> tuple[int, int, int, int]:
    x_min, x_max, y_min, y_max = 0, 0, 0, 0

    cur_x = 0
    cur_y = 0

    for edge in edges:
        step_x, step_y = STEP[edge.dir]
        cur_x += step_x * edge.length
        cur_y += step_y * edge.length

        x_min = min(x_min, cur_x)
        x_max = max(x_max, cur_x)
        y_min = min(y_min, cur_y)
        y_max = max(y_max, cur_y)

    return x_min, x_max, y_min, y_max


def calculate_area_from_edges(edges: list[Edge]) -> int:
    x_min, _, y_min, _ = get_extremes_from_edges(edges)

    area = 0
    circumference = 0

    cur_x = 0
    cur_y = 0

    for i, edge in enumerate(edges):
        step_x, step_y = STEP[edge.dir]
        cur_x += step_x * edge.length
        cur_y += step_y * edge.length

        area += (-1 if (i % 2) else 1) * (cur_x - x_min) * (cur_y - y_min)
        circumference += edge.length

    return abs(area) + (circumference // 2) + 1


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(18)
    logger.info(f"{lines[:3]=}...")

    edges = [Edge(line) for line in lines]

    res_1 = calculate_area_from_edges(edges)
    logger.info(f"{res_1=}")

    long_edges = [edge.transform_by_color() for edge in edges]
    res_2 = calculate_area_from_edges(long_edges)
    logger.info(f"{res_2=}")

    return res_1, res_2
