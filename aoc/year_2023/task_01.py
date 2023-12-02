import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def replace_first(line: str) -> str:
    pos = len(line)
    digit = "one"
    for k in DIGITS:
        where = line.find(k)
        if where != -1 and where < pos:
            digit = k
            pos = where
    return line.replace(digit, str(DIGITS[digit]), 1)


def replace_last(line: str) -> str:
    line = line[::-1]
    pos = len(line)
    digit = "one"
    for k in DIGITS:
        where = line.find(k[::-1])
        if where != -1 and where < pos:
            digit = k
            pos = where
    return line.replace(digit[::-1], str(DIGITS[digit]), 1)[::-1]


def get_digits(line: str, second_task: bool = False) -> list[int]:
    if second_task:
        line = replace_first(line)
        line = replace_last(line)
    return list(int(x) for x in filter(lambda s: s.isdigit(), line))


def get_first_last_as_two_digit(digits: list[int]) -> int:
    first = digits[0]
    last = digits[-1]
    return first * 10 + last


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(1)
    logger.info(f"{lines[:3]=}...")

    res_1 = sum(get_first_last_as_two_digit(get_digits(line)) for line in lines)
    logger.info(f"{res_1=}")

    res_2 = sum(
        get_first_last_as_two_digit(get_digits(line, second_task=True))
        for line in lines
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
