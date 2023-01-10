import logging
from collections import defaultdict

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize

logger = logging.getLogger(__name__)


def count_overlaps(
    ends: list[list[tuple[int, int]]], diagonal: bool = False
) -> dict[tuple[int, int], int]:
    counts: dict[tuple[int, int], int] = defaultdict(lambda: 0)
    for start, end in ends:
        if not diagonal and not (start[0] == end[0] or start[1] == end[1]):
            continue
        step = (
            (end[0] - start[0]) // abs(end[0] - start[0]) if end[0] != start[0] else 0,
            (end[1] - start[1]) // abs(end[1] - start[1]) if end[1] != start[1] else 0,
        )
        current = start
        while current != end:
            counts[current] += 1
            current = (current[0] + step[0], current[1] + step[1])
        counts[current] += 1

    return counts


def get_res_1(ends: list[list[tuple[int, int]]]) -> int:
    coords_to_count = count_overlaps(ends)
    return sum(1 for v in coords_to_count.values() if v > 1)


def get_res_2(ends: list[list[tuple[int, int]]]) -> int:
    coords_to_count = count_overlaps(ends, diagonal=True)
    return sum(1 for v in coords_to_count.values() if v > 1)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(5)
    ends = tokenize(lines, separator=" -> ")
    end_coordinates = convert(
        ends, converter=lambda x: tuple(int(n) for n in x.split(","))
    )
    logger.info(f"{end_coordinates[:3]=}...")

    res_1 = get_res_1(end_coordinates)
    logger.info(f"{res_1=}")
    res_2 = get_res_2(end_coordinates)
    logger.info(f"{res_2=}")

    return res_1, res_2
