import logging
from collections import defaultdict
from itertools import combinations
from math import gcd

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class Field:
    def __init__(self, lines: list[str]) -> None:
        antennas: dict[str, set[tuple[int, int]]] = defaultdict(set)
        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                if c != ".":
                    antennas[c].add((x, y))
        self.antennas = antennas
        self.n_x = len(lines)
        self.n_y = len(lines[0])

    def antinodes(self, resonants: bool = False) -> dict[str, set[tuple[int, int]]]:
        return {c: self.get_antinodes(a, resonants) for c, a in self.antennas.items()}

    def get_antinodes(
        self, nodes: set[tuple[int, int]], resonants: bool = False
    ) -> set[tuple[int, int]]:
        res = set()
        for l, r in combinations(nodes, 2):
            if resonants:
                res.update(self.get_resonants_of(l, r))
            else:
                res.update(self.get_antinodes_of(l, r))
        return res

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.n_x and 0 <= y < self.n_y

    def add_antinode(
        self,
        point: tuple[int, int],
        diff: tuple[int, int],
        anodes: set[tuple[int, int]],
    ) -> None:
        new_x = point[0] + diff[0]
        new_y = point[1] + diff[1]
        if self.is_inside(new_x, new_y):
            anodes.add((new_x, new_y))

    def get_antinodes_of(
        self, left: tuple[int, int], right: tuple[int, int]
    ) -> set[tuple[int, int]]:
        res: set[tuple[int, int]] = set()
        diff_x = right[0] - left[0]
        diff_y = right[1] - left[1]

        # outside
        self.add_antinode(right, (diff_x, diff_y), res)
        self.add_antinode(left, (-diff_x, -diff_y), res)

        # inside
        if (abs(diff_x) % 3) or (abs(diff_y) % 3):
            return res
        step_x = diff_x // 3
        step_y = diff_y // 3
        self.add_antinode(left, (step_x, step_y), res)
        self.add_antinode(right, (-step_x, -step_y), res)

        return res

    def get_resonants_of(
        self, left: tuple[int, int], right: tuple[int, int]
    ) -> set[tuple[int, int]]:
        res = set()
        diff_x = right[0] - left[0]
        diff_y = right[1] - left[1]

        d = gcd(diff_x, diff_y)

        diff_x = diff_x // d
        diff_y = diff_y // d

        next_x = left[0]
        next_y = left[1]
        # left
        while self.is_inside(next_x, next_y):
            res.add((next_x, next_y))
            next_x -= diff_x
            next_y -= diff_y

        # right
        next_x = left[0] + diff_x
        next_y = left[1] + diff_y

        while self.is_inside(next_x, next_y):
            res.add((next_x, next_y))
            next_x += diff_x
            next_y += diff_y

        return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(8)
    logger.info(f"{lines[:3]=}...")

    field = Field(lines)

    res_1 = len(
        set(
            node
            for antinodes in field.antinodes(resonants=False).values()
            for node in antinodes
        )
    )
    logger.info(f"{res_1=}")

    res_2 = len(
        set(
            node
            for antinodes in field.antinodes(resonants=True).values()
            for node in antinodes
        )
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
