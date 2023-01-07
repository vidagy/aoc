import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize

logger = logging.getLogger(__name__)


def move(
    start_x: int, start_depth: int, lines: list[tuple[str, int]]
) -> tuple[int, int]:
    for direction, count in lines:
        if direction == "forward":
            start_x += count
        elif direction == "up":
            start_depth -= count
        elif direction == "down":
            start_depth += count
        else:
            raise Exception("not implemented")
    return start_x, start_depth


def move_2(
    start_x: int, start_depth: int, lines: list[tuple[str, int]]
) -> tuple[int, int]:
    aim = 0
    for direction, count in lines:
        if direction == "forward":
            start_x += count
            start_depth += count * aim
        elif direction == "up":
            aim -= count
        elif direction == "down":
            aim += count
        else:
            raise Exception("not implemented")
    return start_x, start_depth


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = [(d, int(n)) for d, n in tokenize(reader.file_to_lines(2), separator=" ")]
    logger.info(f"{lines[:3]=}...")
    start_x, start_depth = 0, 0

    end_x, end_depth = move(start_x, start_depth, lines)
    res_1 = end_x * end_depth
    logger.info(f"{res_1=}")

    end_2_x, end_2_depth = move_2(start_x, start_depth, lines)
    res_2 = end_2_x * end_2_depth
    logger.info(f"{res_2=}")

    return res_1, res_2
