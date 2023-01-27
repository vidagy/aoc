import logging
import math
import re

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def parse(line: str) -> tuple[int, int, int, int]:
    rex = re.compile(
        r"target area: x=([+\-]?\d+)..([+\-]?\d+), y=([+\-]?\d+)..([+\-]?\d+)"
    )
    x_min, x_max, y_min, y_max = re.findall(rex, line)[0]
    return int(x_min), int(y_min), int(x_max), int(y_max)


def get_max_y(y_min: int, y_max: int) -> int:
    max_v_y = abs(y_min) - 1
    max_y = max_v_y * (max_v_y + 1) // 2
    return max_y


def is_in(x_min: int, y_min: int, x_max: int, y_max: int, v_x: int, v_y: int) -> bool:
    x, y = 0, 0
    t = 0
    while True:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
        if x > x_max or y < y_min:
            return False
        x += v_x
        y += v_y

        v_x -= 1 if v_x > 0 else 0
        v_y -= 1

        t += 1


def get_distinct_velocity_count(x_min: int, y_min: int, x_max: int, y_max: int) -> int:
    max_v_y = abs(y_min) + 10
    max_v_x = x_max + 10
    min_v_x = int(math.sqrt(1 + 8 * x_min) - 1) // 2 - 1 - 10
    counter = 0
    for v_x in range(min_v_x, max_v_x):
        min_v_y = -max_v_y
        for v_y in range(min_v_y, max_v_y):
            if is_in(x_min, y_min, x_max, y_max, v_x, v_y):
                counter += 1
    return counter


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    x_min, y_min, x_max, y_max = parse(reader.file_to_lines(17)[0])
    logger.info(f"{x_min=}, {x_max=}, {y_min=}, {y_max=}")

    res_1 = get_max_y(y_min, y_max)
    logger.info(f"{res_1=}")

    res_2 = get_distinct_velocity_count(x_min, y_min, x_max, y_max)
    logger.info(f"{res_2=}")

    return res_1, res_2
