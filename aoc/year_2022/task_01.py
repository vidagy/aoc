import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, split_lines_by_empty_line

logger = logging.getLogger(__name__)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = split_lines_by_empty_line(reader.file_to_lines(1))
    nums = convert(lines, int)
    logger.info(f"{nums[:3]=}...")

    maxs = sorted([sum(c) for c in nums])

    res_1 = maxs[-1]
    logger.info(f"{res_1=}")
    res_2 = maxs[-1] + maxs[-2] + maxs[-3]
    logger.info(f"{res_2=}")
    return res_1, res_2
