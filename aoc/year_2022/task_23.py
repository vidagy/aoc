import logging
from collections import defaultdict
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


N = Pos(0, -1)
S = Pos(0, 1)
E = Pos(1, 0)
W = Pos(-1, 0)
NE = N + E
NW = N + W
SE = S + E
SW = S + W


class Field:
    def __init__(self, lines: list[str]) -> None:
        self.elves: set[Pos] = set()
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                if c == "#":
                    self.elves.add(Pos(i, j))
        self.dirs = [
            [NE, N, NW],
            [SE, S, SW],
            [NW, W, SW],
            [NE, E, SE],
        ]
        self.dir_index = 0

    @staticmethod
    def get_all_neighbors(elf: Pos) -> set[Pos]:
        return {
            elf + N,
            elf + S,
            elf + E,
            elf + W,
            elf + NE,
            elf + NW,
            elf + SE,
            elf + SW,
        }

    def elves_that_dont_move(self) -> set[Pos]:
        res: set[Pos] = set()
        for elf in self.elves:
            if not self.get_all_neighbors(elf).intersection(self.elves):
                res.add(elf)
        return res

    def move(self, elf: Pos) -> Pos:
        for i in range(4):
            dirs = self.dirs[(self.dir_index + i) % len(self.dirs)]
            dest_poses = {elf + d for d in dirs}
            if not dest_poses.intersection(self.elves):
                return elf + dirs[1]
        return elf

    def evolve(self) -> bool:
        elves_to_move = self.elves.difference(self.elves_that_dont_move())
        # logger.info(f"{len(elves_to_move)=}")

        if not elves_to_move:
            return False
        movements = defaultdict(set)
        for elf in elves_to_move:
            movements[self.move(elf)].add(elf)

        for destination, sources in movements.items():
            if len(sources) == 1:
                elf = next(iter(sources))
                if elf != destination:
                    self.elves.remove(elf)
                    self.elves.add(destination)

        self.dir_index += 1
        return True

    def print(self) -> None:
        min_x = min(e.x for e in self.elves)
        max_x = max(e.x for e in self.elves)
        min_y = min(e.y for e in self.elves)
        max_y = max(e.y for e in self.elves)

        for j in range(min_y, max_y + 1):
            print()
            for i in range(min_x, max_x + 1):
                print("#" if Pos(i, j) in self.elves else ".", end="")

        print()

    def get_res_1(self) -> int:
        min_x = min(e.x for e in self.elves)
        max_x = max(e.x for e in self.elves)
        min_y = min(e.y for e in self.elves)
        max_y = max(e.y for e in self.elves)

        return (max_x - min_x + 1) * (max_y - min_y + 1) - len(self.elves)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(23)
    field = Field(inp)
    # field.print()

    for _ in range(10):
        field.evolve()
        # field.print()

    res_1 = field.get_res_1()
    logger.info(f"{res_1=}")

    i = 11
    while field.evolve():
        i += 1
    res_2 = i
    logger.info(f"{res_2=}")

    return res_1, res_2
