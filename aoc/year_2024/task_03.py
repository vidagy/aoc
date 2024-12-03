import logging
import re

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def extract_matches(line: str) -> list[tuple[int, int]]:
    return re.findall("mul\((\d{1,3}),(\d{1,3})\)", line)


def part_2_matches(line: str) -> list[tuple[int, int]]:
    matches = re.findall("mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)", line)
    do = True
    res = []
    for m in matches:
        if m[2] == "do":
            do = True
            continue
        if m[3] == "don't":
            do = False
            continue
        if do:
            res.append((m[0], m[1]))
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    line = "".join(reader.file_to_lines(3))
    logger.info(f"{line[:30]=}...")

    res_1 = sum(int(match[0]) * int(match[1]) for match in extract_matches(line))
    logger.info(f"{res_1=}")

    res_2 = sum(int(match[0]) * int(match[1]) for match in part_2_matches(line))
    logger.info(f"{res_2=}")

    return res_1, res_2
