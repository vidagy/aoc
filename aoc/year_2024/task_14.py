import logging
import re
from dataclasses import dataclass

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass
class Robot:
    x: int
    y: int
    v_x: int
    v_y: int

    @staticmethod
    def create(line: str) -> "Robot":
        nums = re.findall(r"(\-?\d+)", line)
        assert len(nums) == 4
        return Robot(
            int(nums[0]),
            int(nums[1]),
            int(nums[2]),
            int(nums[3]),
        )

    def evolve(self, time: int, n_x: int, n_y: int) -> None:
        xx = self.x + time * self.v_x
        yy = self.y + time * self.v_y
        self.x = xx % n_x
        self.y = yy % n_y


class Floor:
    def __init__(self, lines: list[str], n_x: int, n_y: int) -> None:
        self.robots: list[Robot] = [Robot.create(line) for line in lines]
        self.n_x = n_x
        self.n_y = n_y
        self.num_evolved = 0

    def safety_factor(self) -> int:
        quads = [[0, 0], [0, 0]]
        b_x = self.n_x // 2
        b_y = self.n_y // 2

        def quad(robot: Robot) -> tuple[int, int]:
            return int(robot.x < b_x), int(robot.y < b_y)

        for robot in self.robots:
            if robot.x == b_x or robot.y == b_y:
                continue
            i, j = quad(robot)
            quads[i][j] += 1
        return quads[0][0] * quads[1][0] * quads[0][1] * quads[1][1]

    def evolve(self, time: int) -> None:
        for robot in self.robots:
            robot.evolve(time, self.n_x, self.n_y)
        self.num_evolved += time

    def has_tree(self) -> bool:
        subtree = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        res = [[" " for _ in range(self.n_x)] for _ in range(self.n_y)]

        for robot in self.robots:
            res[robot.y][robot.x] = "X"

        return any(subtree in "".join(line) for line in res)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(14)
    logger.info(f"{lines[:3]=}...")

    floor = Floor(lines, 101, 103)
    floor.evolve(100)

    res_1 = floor.safety_factor()
    logger.info(f"{res_1=}")

    while not floor.has_tree():
        floor.evolve(1)

    res_2 = floor.num_evolved
    logger.info(f"{res_2=}")

    return res_1, res_2
