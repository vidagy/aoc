import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    numbers = [int(line) for line in reader.file_to_lines(1)]
    logger.info(f"{numbers[:3]=}...")
    res_1 = sum(1 for p in zip(numbers[0:-1], numbers[1:]) if p[1] > p[0])
    logger.info(f"{res_1=}")
    windows = [
        numbers[0 + i] + numbers[1 + i] + numbers[2 + i]
        for i in range(0, len(numbers) - 2)
    ]
    res_2 = sum(1 for p in zip(windows[0:-1], windows[1:]) if p[1] > p[0])
    logger.info(f"{res_2=}")

    return res_1, res_2
