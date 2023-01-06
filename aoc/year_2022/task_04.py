import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize

logger = logging.getLogger(__name__)


def does_contain(left_1, right_1, left_2, right_2) -> bool:
    return (left_1 <= left_2 and right_1 >= right_2) or (
        left_1 >= left_2 and right_1 <= right_2
    )


def has_overlap(left_1, right_1, left_2, right_2) -> bool:
    return not (right_1 < left_2 or right_2 < left_1)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_lines = reader.file_to_lines(4)
    raw_lines = [line.replace(",", "-") for line in raw_lines]
    lines = convert(tokenize(raw_lines, separator="-"), int)
    logger.info(f"{lines[:3]=}...")

    contains = [does_contain(*line) for line in lines]
    logger.info(f"{contains[:3]=}...")
    res_1 = sum(1 for c in contains if c)
    logger.info(f"{res_1=}")

    overlap = [has_overlap(*line) for line in lines]
    logger.info(f"{overlap[:3]=}...")
    res_2 = sum(1 for o in overlap if o)
    logger.info(f"{res_2=}")

    return res_1, res_2
