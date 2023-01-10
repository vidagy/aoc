import logging
from collections import Counter, defaultdict

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def evolve(fish: dict[int, int]) -> dict[int, int]:
    new_fish = defaultdict(lambda: 0)
    for timer, c in fish.items():
        if timer > 0:
            new_fish[timer - 1] += c
        if timer == 0:
            new_fish[6] += c
            new_fish[8] += c

    return  new_fish


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = [int(n) for n in reader.file_to_lines(6)[0].split(",")]
    logger.info(f"{lines[:3]=}...")

    fish = Counter(lines)

    for i in range(80):
        fish = evolve(fish)
    res_1 = sum(fish.values())
    logger.info(f"{res_1=}")

    fish = Counter(lines)
    for i in range(256):
        fish = evolve(fish)
    res_2 = sum(fish.values())
    logger.info(f"{res_2=}")

    return res_1, res_2
