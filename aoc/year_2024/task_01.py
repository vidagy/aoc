import logging
from collections import Counter

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize, transpose

logger = logging.getLogger(__name__)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    left, right = convert(
        transpose(tokenize(reader.file_to_lines(1), separator=" ")), int
    )
    logger.info(f"{left[:3]=}...")
    logger.info(f"{right[:3]=}...")

    left.sort()
    right.sort()

    res_1 = 0
    for l, r in zip(left, right):
        res_1 += abs(l - r)
    logger.info(f"{res_1=}")

    counter = Counter(right)
    res_2 = 0

    for l in left:
        res_2 += l * counter[l]
    logger.info(f"{res_2=}")

    return res_1, res_2
