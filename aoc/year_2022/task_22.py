import logging
import re
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

DIFF = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


class Plan:
    def __init__(self, raw_plan: list[str]) -> None:
        self.y_max = len(raw_plan)
        self.x_max = max(len(line) for line in raw_plan)

        self.walls: list[list[Optional[bool]]] = []
        for j in range(self.y_max):
            self.walls.append([None for i in range(self.x_max)])

        for j in range(self.y_max):
            for i, c in enumerate(raw_plan[j]):
                if c == " ":
                    pass
                elif c == ".":
                    self.walls[j][i] = False
                elif c == "#":
                    self.walls[j][i] = True
                else:
                    raise Exception("Not implemented")

        self.pos: tuple[int, int] = (self.walls[0].index(False), 0)
        self.direction: int = RIGHT

    def turn(self, to: str) -> None:
        if to == "R":
            self.direction = (self.direction + 1) % 4
        elif to == "L":
            self.direction = (4 + self.direction - 1) % 4
        # logger.info(f"{to=} {self.direction}")

    def do_step(
        self, current_pos: tuple[int, int], current_dir: int
    ) -> tuple[tuple[int, int], int]:
        # logger.info("old step")
        current_pos = (
            (current_pos[0] + DIFF[self.direction][0]) % self.x_max,
            (current_pos[1] + DIFF[self.direction][1]) % self.y_max,
        )
        return current_pos, current_dir

    def step(self, how_many: int) -> None:
        steps_done = 0
        # orig_pos = self.pos
        current_pos = self.pos
        # orig_dir = self.direction
        current_dir = self.direction

        while steps_done < how_many:
            while True:
                current_pos, current_dir = self.do_step(current_pos, current_dir)
                what = self.walls[current_pos[1]][current_pos[0]]
                if what is not None:
                    break
            if what:
                break
            elif not what:
                self.pos = current_pos
                self.direction = current_dir
                steps_done += 1
            else:
                raise Exception("Not implemented")

        # logger.info(f"{how_many} => {steps_done} | {orig_dir} <> {current_dir} | {orig_pos} -{'-' if steps_done == how_many else '#'}> {self.pos=}")
        return


class Plan2(Plan):
    def __init__(self, raw_plan: list[str]) -> None:
        super().__init__(raw_plan)
        self.size = self.x_max // 3

    def do_step(
        self, current_pos: tuple[int, int], current_dir: int
    ) -> tuple[tuple[int, int], int]:
        #  21
        #  3
        # 54
        # 6

        # facing:
        # 3: front
        # 2: top
        # 1: right
        # 4: bottom
        # 5: left
        # 6: back

        x = current_pos[0]
        y = current_pos[1]
        S = self.size

        if S <= x < 2 * S and y == 0 and current_dir == UP:
            # logger.info("upper boundary of 2 into 6 from left")
            current_dir = RIGHT
            rel_x = x - S
            current_pos = (0, 3 * S + rel_x)
        elif 2 * S <= x and y == 0 and current_dir == UP:
            # logger.info("upper boundary of 1 into 6 from bottom")
            current_dir = UP
            rel_x = x - 2 * S
            current_pos = (0 + rel_x, 4 * S - 1)
        elif x < S and y == 2 * S and current_dir == UP:
            # logger.info("upper boundary of 5 into 3 from left")
            current_dir = RIGHT
            rel_x = x
            current_pos = (S, S + rel_x)
        elif x < S and y == 4 * S - 1 and current_dir == DOWN:
            # logger.info("lower boundary of 6 into 1 from top")
            current_dir = DOWN
            rel_x = x
            current_pos = (2 * S + rel_x, 0)
        elif S <= x < 2 * S and y == 3 * S - 1 and current_dir == DOWN:
            # logger.info("lower boundary of 4 into 6 from right")
            current_dir = LEFT
            rel_x = x - S
            current_pos = (S - 1, 3 * S + rel_x)
        elif 2 * S <= x and y == S - 1 and current_dir == DOWN:
            # logger.info("lower boundary of 1 into 3 from right")
            current_dir = LEFT
            rel_x = x - 2 * S
            current_pos = (2 * S - 1, S + rel_x)
        elif x == 0 and 3 * S <= y and current_dir == LEFT:
            # logger.info("left boundary of 6 into 2 from top")
            current_dir = DOWN
            rel_y = y - 3 * S
            current_pos = (S + rel_y, 0)
        elif x == 0 and 2 * S <= y < 3 * S and current_dir == LEFT:
            # logger.info("left boundary of 5 into 2 from left")
            current_dir = RIGHT
            rel_y = y - 2 * S
            current_pos = (S, S - 1 - rel_y)
        elif x == S and S <= y < 2 * S and current_dir == LEFT:
            # logger.info("left boundary of 3 into 5 from top")
            current_dir = DOWN
            rel_y = y - S
            current_pos = (rel_y, 2 * S)
        elif x == S and 0 <= y < S and current_dir == LEFT:
            # logger.info("left boundary of 2 into 5 from left")
            current_dir = RIGHT
            rel_y = y
            current_pos = (0, 3 * S - 1 - rel_y)
        elif x == S - 1 and 3 * S <= y and current_dir == RIGHT:
            # logger.info("right boundary of 6 into 4 from bottom")
            current_dir = UP
            rel_y = y - 3 * S
            current_pos = (S + rel_y, 3 * S - 1)
        elif x == 2 * S - 1 and 2 * S <= y < 3 * S and current_dir == RIGHT:
            # logger.info("right boundary of 4 int 1 from right")
            current_dir = LEFT
            rel_y = y - 2 * S
            current_pos = (3 * S - 1, S - 1 - rel_y)
        elif x == 2 * S - 1 and S <= y < 2 * S and current_dir == RIGHT:
            # logger.info("right boundary of 3 into 1 from bottom")
            current_dir = UP
            rel_y = y - S
            current_pos = (2 * S + rel_y, S - 1)
        elif x == 3 * S - 1 and y < S and current_dir == RIGHT:
            # logger.info("right boundary of 1 into 4 from right")
            current_dir = LEFT
            rel_y = y
            current_pos = (2 * S - 1, 3 * S - 1 - rel_y)
        else:
            return super().do_step(current_pos, current_dir)

        return current_pos, current_dir


@dataclass
class Instruction:
    @abstractmethod
    def do(self, plan: Plan) -> None:
        pass

    @staticmethod
    def parse_line(line: str) -> list["Instruction"]:
        reg = re.compile(r"([0-9]+|[RL])")
        all_matches = reg.findall(line)
        instructions = [
            Walk(int(match)) if match.isnumeric() else Turn(match)
            for match in all_matches
        ]
        return instructions


@dataclass
class Turn(Instruction):
    direction: str

    def do(self, plan: Plan) -> None:
        plan.turn(self.direction)

    def __repr__(self) -> str:
        return self.direction


@dataclass
class Walk(Instruction):
    steps: int

    def do(self, plan: Plan) -> None:
        plan.step(self.steps)

    def __repr__(self) -> str:
        return f"{self.steps}"


def parse_input(lines: list[str]) -> tuple[Plan, list[Instruction]]:
    inp = split_lines_by_empty_line(lines)
    inp_map = inp[0]
    inp_instructions = inp[1][0]

    return Plan(inp_map), Instruction.parse_line(inp_instructions)


def parse_input_2(lines: list[str]) -> tuple[Plan, list[Instruction]]:
    inp = split_lines_by_empty_line(lines)
    inp_map = inp[0]
    inp_instructions = inp[1][0]

    return Plan2(inp_map), Instruction.parse_line(inp_instructions)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(22)
    plan, instructions = parse_input(inp)
    # logger.info(f"{len(plan.walls[0])=} {len(plan.walls)=}")
    # logger.info(f"{len(instructions)=}")
    for instruction in instructions:
        instruction.do(plan)

    res_1 = 1000 * (1 + plan.pos[1]) + 4 * (1 + plan.pos[0]) + plan.direction
    # logger.info(f"{res_1=}")

    plan2, _ = parse_input_2(inp)
    for instruction in instructions:
        instruction.do(plan2)

    res_2 = 1000 * (1 + plan2.pos[1]) + 4 * (1 + plan2.pos[0]) + plan2.direction
    # logger.info(f"{res_2=}")

    return res_1, res_2
