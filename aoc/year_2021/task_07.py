import logging
from typing import Callable

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def middle(positions: list[int], cost: Callable[[int], int]) -> int:
    minp = min(positions)
    maxp = max(positions)
    min_diff = sum(cost(p) for p in positions)
    for mid in range(minp, maxp + 1):
        this_diff = sum(cost(p - mid) for p in positions)
        min_diff = min(min_diff, this_diff)

    return min_diff


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(7)
    lines = [int(n) for n in inp[0].split(",")]
    logger.info(f"{lines[:3]=}...")

    res_1 = middle(lines, cost=lambda d: abs(d))
    logger.info(f"{res_1=}")

    res_2 = middle(lines, cost=lambda d: abs(d) * (abs(d) + 1) // 2)
    logger.info(f"{res_2=}")

    return res_1, res_2
