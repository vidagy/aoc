import logging
from dataclasses import dataclass

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

DIFF = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]


@dataclass(frozen=True, unsafe_hash=True)
class Blizzard:
    dir: int
    x: int
    y: int

    @staticmethod
    def create_fror_raw(dir: str, x: int, y: int) -> "Blizzard":
        if dir == ">":
            return Blizzard(RIGHT, x, y)
        elif dir == "v":
            return Blizzard(DOWN, x, y)
        elif dir == "<":
            return Blizzard(LEFT, x, y)
        elif dir == "^":
            return Blizzard(UP, x, y)
        else:
            raise Exception("not implemented" + f"{dir=}")

    def __repr__(self) -> str:
        return f"{self.dir}[{self.x},{self.y}]"


@dataclass(frozen=True, unsafe_hash=True)
class Pos:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"


@dataclass(frozen=True, unsafe_hash=True)
class State:
    time: int
    blizzards: list[Blizzard]
    x_min: int
    x_size: int
    y_min: int
    y_size: int

    @staticmethod
    def create_from_raw(
        lines: list[str],
    ) -> tuple["State", Pos, Pos]:
        y_min = 1
        y_size = len(lines) - 2
        x_min = 1
        x_size = len(lines[0]) - 2

        for i, c in enumerate(lines[0]):
            if c == ".":
                starting_pos = Pos(i, 0)

        blizzards: list[Blizzard] = []
        for j in range(1, len(lines) - 1):
            for i, c in enumerate(lines[j]):
                if c in {">", "<", "v", "^"}:
                    blizzards.append(Blizzard.create_fror_raw(c, i, j))

        for i, c in enumerate(lines[-1]):
            if c == ".":
                destination = Pos(i, len(lines) - 1)

        return (
            State(
                time=0,
                blizzards=blizzards,
                x_min=x_min,
                x_size=x_size,
                y_min=y_min,
                y_size=y_size,
            ),
            starting_pos,
            destination,
        )

    def _evolve_blizzard(self, blizzard: Blizzard) -> Blizzard:
        return Blizzard(
            blizzard.dir,
            (blizzard.x - self.x_min + DIFF[blizzard.dir][0]) % self.x_size
            + self.x_min,
            (blizzard.y - self.y_min + DIFF[blizzard.dir][1]) % self.y_size
            + self.y_min,
        )

    def evolve(self) -> "State":
        new_blizzards = [self._evolve_blizzard(b) for b in self.blizzards]
        return State(
            time=self.time + 1,
            blizzards=new_blizzards,
            x_min=self.x_min,
            x_size=self.x_size,
            y_min=self.y_min,
            y_size=self.y_size,
        )

    def get_available_pos(
        self, pre_pos: set[Pos], start: Pos, destination: Pos
    ) -> set[Pos]:
        available_pos = {
            n for pos in pre_pos for n in self.get_neighbors(pos, start, destination)
        }.difference(Pos(b.x, b.y) for b in self.blizzards)
        return available_pos

    def get_neighbors(self, pos: Pos, start: Pos, destination: Pos) -> set[Pos]:
        all_neighbors = [Pos(pos.x + d[0], pos.y + d[1]) for d in DIFF]

        def f(pos: Pos) -> bool:
            return (
                (
                    self.x_min <= pos.x < self.x_min + self.x_size
                    and self.y_min <= pos.y < self.y_min + self.y_size
                )
                or pos == start
                or pos == destination
            )

        return set(filter(f, all_neighbors))


def get_res_1(state: State, start: Pos, destination: Pos) -> State:
    rounds = state.time
    current_pos = {start}
    while destination not in current_pos:
        rounds += 1
        logger.info(f"{rounds=}")
        state = state.evolve()
        next_pos = state.get_available_pos(current_pos, start, destination)

        # logger.info(f"{next_pos=}")
        current_pos = next_pos

    return state


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(24)
    state, starting_pos, destination = State.create_from_raw(inp)
    logger.info(f"{starting_pos=}, {destination=}")

    state = get_res_1(state, starting_pos, destination)
    res_1 = state.time
    logger.info(f"{res_1=}")

    state = get_res_1(state, destination, starting_pos)
    state = get_res_1(state, starting_pos, destination)
    res_2 = state.time
    logger.info(f"{res_2=}")

    return res_1, res_2
