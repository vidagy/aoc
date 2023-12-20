import logging
from dataclasses import dataclass
from enum import Enum

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


EMPTY = "."
ROCK = "#"
PEBBLE = "O"


class Direction(Enum):
    NORTH = 1
    EAST = 2
    WEST = 3
    SOUTH = 4


RangeT = tuple[int, int, int]
StepT = tuple[int, int]


STEP: dict[Direction, StepT] = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.WEST: (0, -1),
    Direction.SOUTH: (1, 0),
}


@dataclass
class Platform:
    data: list[list[str]]

    def __repr__(self) -> str:
        return "\n" + "\n".join("".join(line) for line in self.data) + "\n"

    def __init__(self, lines: list[str]) -> None:
        self.data = [list(line) for line in lines]
        self.n_x = len(self.data)
        self.n_y = len(self.data[0])

    def enumerator(
        self, direction: Direction, first_frame: bool = False, second_frame: bool = True
    ) -> tuple[list[StepT], list[StepT]]:
        def x_there(frame: bool) -> list[StepT]:
            return [(i, 0) for i in range(1 - int(frame), self.n_x, 1)]

        def x_back(frame: bool) -> list[StepT]:
            return [(i, 0) for i in range(self.n_x - 2 + int(frame), -1, -1)]

        def y_there(frame: bool) -> list[StepT]:
            return [(0, i) for i in range(1 - int(frame), self.n_y, 1)]

        def y_back(frame: bool) -> list[StepT]:
            return [(0, i) for i in range(self.n_y - 2 + int(frame), -1, -1)]

        if direction == Direction.NORTH:
            return (x_there(first_frame), y_there(second_frame))
        if direction == Direction.SOUTH:
            return (x_back(first_frame), y_there(second_frame))
        if direction == Direction.EAST:
            return (y_back(first_frame), x_there(second_frame))
        if direction == Direction.WEST:
            return (y_there(first_frame), x_there(second_frame))

        raise Exception("Not implemented")

    def _scan(self, direction: Direction) -> int:
        changed = 0
        step_x, step_y = STEP[direction]
        first_range, second_range = self.enumerator(direction)
        for first_x, first_y in first_range:
            for second_x, second_y in second_range:
                current = self.data[first_x + second_x][first_y + second_y]
                next = self.data[first_x + second_x + step_x][
                    first_y + second_y + step_y
                ]

                if current == PEBBLE and next == EMPTY:
                    changed += 1
                    next_step_x = step_x
                    next_step_y = step_y
                    while (
                        0 < next_step_x < self.n_x - 1
                        and 0 < next_step_y < self.n_y - 1
                    ):
                        if (
                            self.data[first_x + second_x + next_step_x + step_x][
                                first_y + second_y + next_step_y + step_y
                            ]
                            == EMPTY
                        ):
                            next_step_x += step_x
                            next_step_y += step_y
                        else:
                            break

                    self.data[first_x + second_x][first_y + second_y] = EMPTY
                    self.data[first_x + second_x + next_step_x][
                        first_y + second_y + next_step_y
                    ] = PEBBLE

        return changed

    def tilt(self, direction: Direction) -> None:
        while self._scan(direction):
            pass

    def get_weight(self, direction: Direction = Direction.NORTH) -> int:
        score = 0
        first_range, second_range = self.enumerator(direction, True, True)
        for i, (first_x, first_y) in enumerate(first_range[::-1], start=1):
            for second_x, second_y in second_range:
                if PEBBLE == self.data[first_x + second_x][first_y + second_y]:
                    score += i

        return score

    def do_cycle(self) -> None:
        for d in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]:
            self.tilt(d)

    @staticmethod
    def find_period(series: list[int]) -> int:
        for i in range(1, len(series) - 1):
            same = True
            for j in range(0, len(series) - i):
                if series[j] != series[j + i]:
                    same = False
                    break
            if same:
                return i
        raise Exception("No period")

    def find_1000000000_cycle(self) -> int:
        scores = [self.get_weight()]
        for _ in range(300):
            self.do_cycle()
            scores.append(self.get_weight())

        periodic_part = scores[170:]

        periodicity = Platform.find_period(periodic_part)
        N = 1000000000 - 170
        remainder = N % periodicity
        return periodic_part[remainder]


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(14)

    platform = Platform(lines)
    platform.tilt(Direction.NORTH)

    res_1 = platform.get_weight()
    logger.info(f"{res_1=}")

    res_2 = platform.find_1000000000_cycle()
    logger.info(f"{res_2=}")

    return res_1, res_2
