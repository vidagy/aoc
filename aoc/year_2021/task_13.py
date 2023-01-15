import logging
import re
from abc import ABC, abstractmethod

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


class Instruction(ABC):
    @staticmethod
    def create(line: str) -> "Instruction":
        rex = r"fold along ([xy])=(\d+)"
        what, where = re.findall(rex, line)[0]
        if what == "x":
            return FoldX(int(where))
        if what == "y":
            return FoldY(int(where))
        raise Exception("cannot parse input")

    @abstractmethod
    def fold(self, point: tuple[int, int]) -> tuple[int, int]:
        raise NotImplementedError()


class FoldX(Instruction):
    def __init__(self, x: int) -> None:
        self.x = x

    def fold(self, point: tuple[int, int]) -> tuple[int, int]:
        x, y = point
        new_x = x if x <= self.x else 2 * self.x - x
        # logger.info(f"{x}, {y} -{self}-> {new_x}, {y}")
        return new_x, y

    def __repr__(self) -> str:
        return f"x[{self.x}]"


class FoldY(Instruction):
    def __init__(self, y: int) -> None:
        self.y = y

    def fold(self, point: tuple[int, int]) -> tuple[int, int]:
        x, y = point
        new_y = y if y <= self.y else 2 * self.y - y
        # logger.info(f"{x}, {y} -{self}-> {x}, {new_y}")
        return x, new_y

    def __repr__(self) -> str:
        return f"y[{self.y}]"


def get_res_2(points: set[tuple[int, int]], instructions: list[Instruction]) -> str:
    for inst in instructions:
        points = {inst.fold(p) for p in points}

    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    res = ""
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if (x, y) in points:
                res += "#"
            else:
                res += " "
        res += "\n"
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, str]:
    inp = reader.file_to_lines(13)
    raw_points, raw_instructions = split_lines_by_empty_line(inp)
    points: set[tuple[int, int]] = {
        tuple(int(n) for n in line.split(",")) for line in raw_points  # type: ignore
    }
    instructions = [Instruction.create(line) for line in raw_instructions]

    res_1 = len({instructions[0].fold(p) for p in points})
    logger.info(f"{res_1=}")

    res_2 = get_res_2(points, instructions)
    logger.info(f"\n{res_2}")

    return res_1, res_2
