import logging
from collections import Counter
from copy import deepcopy

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def get_res_1(lines: list[str]) -> tuple[int, int]:
    most_commons, least_commons = "", ""
    num_digits = len(lines[0])
    for i in range(num_digits):
        counter = Counter([num[i] for num in lines])
        more = max(counter, key=lambda k: counter[k])
        less = min(counter, key=lambda k: counter[k])
        most_commons += more
        least_commons += less
    return int(most_commons, 2), int(least_commons, 2)


def get_res_2(lines: list[str]) -> tuple[int, int]:
    num_digits = len(lines[0])
    current_most_commons, current_least_commons = deepcopy(lines), deepcopy(lines)
    for i in range(num_digits):
        counter_most = Counter([num[i] for num in current_most_commons])
        counter_least = Counter([num[i] for num in current_least_commons])

        digit_most = "0" if counter_most["0"] > counter_most["1"] else "1"
        digit_lest = "1" if counter_least["1"] < counter_least["0"] else "0"

        if len(current_most_commons) > 1:
            current_most_commons = [
                n for n in current_most_commons if n[i] == digit_most
            ]
        if len(current_least_commons) > 1:
            current_least_commons = [
                n for n in current_least_commons if n[i] == digit_lest
            ]

    return int(current_most_commons[0], 2), int(current_least_commons[0], 2)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(3)
    logger.info(f"{lines[:3]=}...")

    most_commons, least_commons = get_res_1(lines)
    res_1 = most_commons * least_commons
    logger.info(f"{res_1=}")

    most_commons, least_commons = get_res_2(lines)
    res_2 = most_commons * least_commons
    logger.info(f"{res_2=}")

    return res_1, res_2
