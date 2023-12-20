import logging
from dataclasses import dataclass
from enum import Enum

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class Direction(Enum):
    Up = 0
    Right = 1
    Left = 2
    Down = 3


StepT = tuple[int, int]

STEP: dict[Direction, StepT] = {
    Direction.Up: (-1, 0),
    Direction.Right: (0, 1),
    Direction.Left: (0, -1),
    Direction.Down: (1, 0),
}


class Tile(Enum):
    Air = "."
    ForwardMirror = "/"
    BackwardMirror = "\\"
    VerticalSplitter = "|"
    HorizontalSplitter = "-"


NEXT_DIRECTIONS: dict[Direction, dict[Tile, list[Direction]]] = {
    Direction.Up: {
        Tile.Air: [Direction.Up],
        Tile.ForwardMirror: [Direction.Right],
        Tile.BackwardMirror: [Direction.Left],
        Tile.VerticalSplitter: [Direction.Up],
        Tile.HorizontalSplitter: [Direction.Left, Direction.Right],
    },
    Direction.Right: {
        Tile.Air: [Direction.Right],
        Tile.ForwardMirror: [Direction.Up],
        Tile.BackwardMirror: [Direction.Down],
        Tile.VerticalSplitter: [Direction.Up, Direction.Down],
        Tile.HorizontalSplitter: [Direction.Right],
    },
    Direction.Left: {
        Tile.Air: [Direction.Left],
        Tile.ForwardMirror: [Direction.Down],
        Tile.BackwardMirror: [Direction.Up],
        Tile.VerticalSplitter: [Direction.Up, Direction.Down],
        Tile.HorizontalSplitter: [Direction.Left],
    },
    Direction.Down: {
        Tile.Air: [Direction.Down],
        Tile.ForwardMirror: [Direction.Left],
        Tile.BackwardMirror: [Direction.Right],
        Tile.VerticalSplitter: [Direction.Down],
        Tile.HorizontalSplitter: [Direction.Left, Direction.Right],
    },
}


State = tuple[tuple[int, int], Direction]


@dataclass
class Cave:
    tiles: list[list[Tile]]

    def wipe(self) -> None:
        self.energized = [
            [[False, False, False, False] for _ in range(self.n_y)]
            for _ in range(self.n_x)
        ]

    def __post_init__(self) -> None:
        self.n_x = len(self.tiles)
        self.n_y = len(self.tiles[0])
        self.wipe()

    def energize(
        self, start: tuple[int, int] = (0, 0), dir: Direction = Direction.Right
    ) -> None:
        backlog: set[State] = set()
        backlog.add((start, dir))
        while backlog:
            (current_x, current_y), current_dir = backlog.pop()

            if self.energized[current_x][current_y][current_dir.value]:
                continue

            current_tile = self.tiles[current_x][current_y]
            next_dirs = NEXT_DIRECTIONS[current_dir][current_tile]
            for next_dir in next_dirs:
                step_x, step_y = STEP[next_dir]
                new_pos_x = current_x + step_x
                new_pos_y = current_y + step_y

                if (
                    0 <= new_pos_x < self.n_x
                    and 0 <= new_pos_y < self.n_y
                    and not self.energized[new_pos_x][new_pos_y][next_dir.value]
                ):
                    backlog.add(((new_pos_x, new_pos_y), next_dir))

            self.energized[current_x][current_y][current_dir.value] = True

    @property
    def num_energized(self) -> int:
        return sum(int(any(tile)) for row in self.energized for tile in row)

    def max_energized(self) -> int:
        res = 0
        for x, dir in [(0, Direction.Down), (self.n_x - 1, Direction.Up)]:
            for y in range(self.n_y):
                self.wipe()
                self.energize((x, y), dir)
                num_energized = self.num_energized
                if num_energized > res:
                    res = num_energized
        for y, dir in [(0, Direction.Right), (self.n_y - 1, Direction.Left)]:
            for x in range(self.n_x):
                self.wipe()
                self.energize((x, y), dir)
                num_energized = self.num_energized
                if num_energized > res:
                    res = num_energized

        return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(16)
    logger.info(f"{lines[:3]=}...")

    cave = Cave([[Tile(c) for c in line] for line in lines])
    cave.energize()

    res_1 = cave.num_energized
    logger.info(f"{res_1=}")

    res_2 = cave.max_energized()
    logger.info(f"{res_2=}")

    return res_1, res_2
