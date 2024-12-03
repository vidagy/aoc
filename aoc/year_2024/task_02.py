import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize

logger = logging.getLogger(__name__)


def all_increasing(line: list[int]) -> bool:
    sort = sorted(line)
    return sort == line


def all_decreasing(line: list[int]) -> bool:
    sort = sorted(line, reverse=True)
    return sort == line


def diff_is_1_3(line: list[int]) -> bool:
    pre = line[0]
    for next in line[1:]:
        if not (1 <= abs(next - pre) <= 3):
            return False
        pre = next
    return True


def is_safe(line: list[int], dampener: bool = False) -> bool:
    assert len(line) > 1

    _is_safe = all(
        [
            any(
                [
                    all_increasing(line),
                    all_decreasing(line),
                ]
            ),
            diff_is_1_3(line),
        ]
    )

    if _is_safe or not dampener:
        return _is_safe

    return any([is_safe(line[:i] + line[i + 1 :]) for i in range(len(line))])


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = convert(tokenize(reader.file_to_lines(2), separator=" "), int)
    logger.info(f"{lines[:3]=}...")

    res_1 = sum(is_safe(line) for line in lines)
    logger.info(f"{res_1=}")

    res_2 = sum(is_safe(line, dampener=True) for line in lines)
    logger.info(f"{res_2=}")

    return res_1, res_2
