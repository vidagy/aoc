import logging
from math import log10
from typing import Optional

import cachetools

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize

logger = logging.getLogger(__name__)


def evolve(stone: int) -> tuple[int, Optional[int]]:
    if stone == 0:
        return 1, None
    digits = int(log10(stone) + 1)
    if not (digits % 2):
        boundary = 10 ** (digits // 2)
        other = stone % boundary
        return stone // boundary, other
    return stone * 2024, None


@cachetools.cached(cache=cachetools.LRUCache(maxsize=1000000))
def len_evolve_n_times(stone: Optional[int], n: int) -> int:
    if stone is None:
        return 0
    if n == 0:
        return 1
    res1, res2 = evolve(stone)
    return len_evolve_n_times(res1, n - 1) + len_evolve_n_times(res2, n - 1)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    numbers = convert(tokenize(reader.file_to_lines(11), separator=" "), int)[0]
    logger.info(f"{numbers=}")

    res_1 = sum(len_evolve_n_times(n, 25) for n in numbers)
    logger.info(f"{res_1=}")

    res_2 = sum(len_evolve_n_times(n, 75) for n in numbers)
    logger.info(f"{res_2=}")

    return res_1, res_2
