import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize_by_char

logger = logging.getLogger(__name__)


def get_neighbors(x: int, y: int, width: int, height: int) -> list[tuple[int, int]]:
    x_n = [(xx, y) for xx in [x + 1, x - 1] if 0 <= xx < width]
    y_n = [(x, yy) for yy in [y + 1, y - 1] if 0 <= yy < height]
    return x_n + y_n


def get_min_positions(mapping: list[list[int]]) -> list[tuple[int, int]]:
    height = len(mapping)
    width = len(mapping[0])

    res: list[tuple[int, int]] = []

    for x in range(width):
        for y in range(height):
            this = mapping[y][x]
            neighbors = [
                mapping[ny][nx] for nx, ny in get_neighbors(x, y, width, height)
            ]
            if all(this < n for n in neighbors):
                res.append((x, y))
    return res


def measure_basins(
    mapping: list[list[int]], min_positions: list[tuple[int, int]]
) -> list[int]:
    height = len(mapping)
    width = len(mapping[0])

    res = []

    for x, y in min_positions:
        already_visited: set[tuple[int, int]] = set()
        to_visit: set[tuple[int, int]] = set()

        to_visit.add((x, y))
        while to_visit:
            xx, yy = to_visit.pop()
            if (xx, yy) in already_visited:
                continue
            n = get_neighbors(xx, yy, width, height)
            for xxx, yyy in n:
                if mapping[yyy][xxx] != 9 and (xxx, yyy) not in already_visited:
                    to_visit.add((xxx, yyy))
            already_visited.add((xx, yy))
        res.append(len(already_visited))

    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    mapping = convert(tokenize_by_char(reader.file_to_lines(9)), int)

    min_positions = get_min_positions(mapping)
    res_1 = sum(1 + mapping[y][x] for x, y in min_positions)
    logger.info(f"{res_1=}")

    basin_sizes = sorted(measure_basins(mapping, min_positions), reverse=True)
    res_2 = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
    logger.info(f"{res_2=}")

    return res_1, res_2
