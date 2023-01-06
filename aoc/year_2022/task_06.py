import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    line = reader.file_to_lines(6)[0]
    logger.info(f"{line=}")

    for i in range(4, len(line)):
        if len(set(line[i - 4 : i])) == 4:
            res_1 = i
            break

    logger.info(f"{res_1=}")

    for i in range(14, len(line)):
        if len(set(line[i - 14 : i])) == 14:
            res_2 = i
            break

    logger.info(f"{res_2=}")

    return res_1, res_2
