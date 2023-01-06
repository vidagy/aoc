import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def letter_to_point(letter: str):
    if letter == letter.upper():
        return ord(letter) - ord("A") + 27
    if letter == letter.lower():
        return ord(letter) - ord("a") + 1


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(3)
    logger.info(f"{lines[:3]=}...")
    two_lines = [[line[0 : len(line) // 2], line[len(line) // 2 :]] for line in lines]
    logger.info(f"{two_lines[:3]=}...")
    diff = [set(tl[0]).intersection(tl[1]) for tl in two_lines]
    logger.info(f"{diff[:3]=}...")

    result = sum(letter_to_point(line) for row in diff for line in row)
    logger.info(f"{result=}...")

    ###

    groups = []
    for i in range(len(lines) // 3):
        groups.append([set(lines[3 * i]), set(lines[3 * i + 1]), set(lines[3 * i + 2])])
    logger.info(f"{groups[:3]=}...")

    items = [group[0].intersection(group[1]).intersection(group[2]) for group in groups]
    logger.info(f"{items[:3]=}...")

    result2 = sum(letter_to_point(line) for row in items for line in row)
    logger.info(f"{result2=}...")

    return result, result2
