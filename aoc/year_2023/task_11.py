import logging
from dataclasses import dataclass

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass(frozen=True, unsafe_hash=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def distance(self, other: "Pos") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Galaxies:
    galaxies: list[Pos]

    @staticmethod
    def empty_lines(lines: list[str]) -> set[int]:
        res = set()
        for x, line in enumerate(lines):
            if all(c == "." for c in line):
                res.add(x)
        return res

    @staticmethod
    def empty_cols(lines: list[str]) -> set[int]:
        res = set()
        for i in range(len(lines[0])):
            col = [line[i] for line in lines]
            if all(c == "." for c in col):
                res.add(i)
        return res

    @staticmethod
    def create(lines: list[str], expansion: int) -> "Galaxies":
        empty_lines = Galaxies.empty_lines(lines)
        empty_cols = Galaxies.empty_cols(lines)

        passed_empty_rows = 0

        res = []
        for x, line in enumerate(lines):
            if x in empty_lines:
                passed_empty_rows += 1
                continue

            passed_empty_cols = 0
            for y, c in enumerate(line):
                if y in empty_cols:
                    passed_empty_cols += 1
                    continue
                if c == "#":
                    res.append(
                        Pos(
                            x - passed_empty_rows + expansion * passed_empty_rows,
                            y - passed_empty_cols + expansion * passed_empty_cols,
                        )
                    )

        return Galaxies(res)

    def calculate_all_distances(self) -> int:
        res = 0
        for i, g in enumerate(self.galaxies):
            for gg in self.galaxies[i:]:
                res += g.distance(gg)
        return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(11)
    logger.info(f"{lines[:3]=}...")
    galaxies = Galaxies.create(lines, expansion=2)

    res_1 = galaxies.calculate_all_distances()
    logger.info(f"{res_1=}")

    galaxies = Galaxies.create(lines, expansion=int(1e6))
    res_2 = galaxies.calculate_all_distances()
    logger.info(f"{res_2=}")

    return res_1, res_2
