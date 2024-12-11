import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize_by_char

logger = logging.getLogger(__name__)


DIR_TO_CHAR = {
    (-1, 0): "^",
    (0, 1): ">",
    (1, 0): "v",
    (0, -1): "<",
}


class LoopException(Exception):
    pass


class Guard:

    @staticmethod
    def from_lines(lines: list[list[str]]) -> "Guard":
        n_x = len(lines)
        n_y = len(lines[0])
        start_pos = Guard.find_current_pos(lines)
        obstructions = Guard.get_obstructions(lines)

        return Guard(n_x, n_y, start_pos, obstructions)

    def __init__(
        self,
        n_x: int,
        n_y: int,
        current_pos: tuple[int, int],
        obstructions: set[tuple[int, int]],
    ) -> None:
        self.obstructions = obstructions
        self.n_x = n_x
        self.n_y = n_y

        self.current_dir = (-1, 0)
        self.current_pos = current_pos

        self.positions: set[tuple[int, int, str]] = {
            (self.current_pos[0], self.current_pos[1], DIR_TO_CHAR[self.current_dir])
        }

    @staticmethod
    def get_obstructions(lines: list[list[str]]) -> set[tuple[int, int]]:
        res = set()
        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                if c == "#":
                    res.add((x, y))
        return res

    @staticmethod
    def find_current_pos(lines: list[list[str]]) -> tuple[int, int]:
        for x in range(len(lines)):
            for y in range(len(lines[0])):
                if lines[x][y] == "^":
                    return (x, y)
        raise Exception("Input expected to contain start position")

    @staticmethod
    def print(pos: tuple[int, int], dir: tuple[int, int]) -> str:
        return f"[{pos[0]:3d} {pos[1]:3d}] ({dir[0]:+1d} {dir[1]:+1d})"

    def turn_right(self) -> None:
        new_dir = (self.current_dir[1], -1 * self.current_dir[0])
        # logger.info(f"{self.print(self.current_pos, self.current_dir)} ->  TURN -> {self.print(self.current_pos, new_dir)}")
        self.current_dir = new_dir
        self.positions.add(
            (self.current_pos[0], self.current_pos[1], DIR_TO_CHAR[self.current_dir])
        )

    def step(self) -> None:
        next_pos_x = self.current_pos[0] + self.current_dir[0]
        next_pos_y = self.current_pos[1] + self.current_dir[1]

        # logger.info(f"{self.print(self.current_pos, self.current_dir)} ->  STEP -> {self.print((next_pos_x, next_pos_y), self.current_dir)}")

        assert (next_pos_x, next_pos_y) not in self.obstructions
        self.current_pos = (next_pos_x, next_pos_y)
        self.positions.add(
            (self.current_pos[0], self.current_pos[1], DIR_TO_CHAR[self.current_dir])
        )

    def would_leave(self) -> bool:
        next_pos_x = self.current_pos[0] + self.current_dir[0]
        next_pos_y = self.current_pos[1] + self.current_dir[1]

        return (
            next_pos_x < 0
            or next_pos_x >= self.n_x
            or next_pos_y < 0
            or next_pos_y >= self.n_y
        )

    def is_something_in_front(self) -> bool:
        next_pos_x = self.current_pos[0] + self.current_dir[0]
        next_pos_y = self.current_pos[1] + self.current_dir[1]

        return (next_pos_x, next_pos_y) in self.obstructions

    def would_step_into_loop(self) -> bool:
        next_pos_x = self.current_pos[0] + self.current_dir[0]
        next_pos_y = self.current_pos[1] + self.current_dir[1]

        return (next_pos_x, next_pos_y, DIR_TO_CHAR[self.current_dir]) in self.positions

    def would_turn_into_loop(self) -> bool:
        new_dir = (self.current_dir[1], -1 * self.current_dir[0])
        return (
            self.current_pos[0],
            self.current_pos[1],
            DIR_TO_CHAR[new_dir],
        ) in self.positions

    def walk(self) -> "Guard":
        while not self.would_leave():
            if self.is_something_in_front():
                if self.would_turn_into_loop():
                    raise LoopException()
                self.turn_right()
            else:
                if self.would_step_into_loop():
                    raise LoopException()
                self.step()
        return self

    def num_visited(self) -> int:
        return len({(x, y) for x, y, _ in self.positions})


def get_loops(guard: Guard, lines: list[list[str]]) -> set[tuple[int, int]]:
    original_pos = Guard.find_current_pos(lines)
    all_pos = {(x, y) for x, y, _ in guard.positions}
    all_pos.remove(original_pos)
    res = set()
    for i, pos in enumerate(all_pos):
        # logger.info(f"{i=} / n={len(all_pos)}")
        this_guard = Guard(
            n_x=guard.n_x,
            n_y=guard.n_y,
            current_pos=original_pos,
            obstructions=guard.obstructions.union({pos}),
        )
        try:
            this_guard.walk()
        except LoopException:
            res.add(pos)
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = tokenize_by_char(reader.file_to_lines(6))
    logger.info(f"{lines[:3]=}...")

    guard = Guard.from_lines(lines).walk()
    res_1 = guard.num_visited()
    logger.info(f"{res_1=}")

    res_2 = len(get_loops(guard, lines))
    logger.info(f"{res_2=}")

    return res_1, res_2
