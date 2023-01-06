import logging
from copy import deepcopy
from typing import Any

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, print_matrix, tokenize_by_char

logger = logging.getLogger(__name__)


def initialize_matrix(size_x: int, size_y: int, value: Any) -> list[list[Any]]:
    res: list[list[int]] = []
    for j in range(size_y):
        res.append([])
        for i in range(size_x):
            res[j].append(deepcopy(value))
    return res


def calculate_max_to_side(lines: list[list[int]]) -> list[list[dict[str, int]]]:
    size_x, size_y = len(lines[0]), len(lines)
    max_to_side: list[list[dict[str, int]]] = initialize_matrix(
        size_x, size_y, {"l": 0, "r": 0, "u": 0, "d": 0}
    )

    # left
    for i in range(1, size_x):
        for j in range(size_y):
            max_to_side[j][i]["l"] = max(max_to_side[j][i - 1]["l"], lines[j][i - 1])

    # right
    for i in range(size_x - 2, -1, -1):
        for j in range(size_y):
            max_to_side[j][i]["r"] = max(max_to_side[j][i + 1]["r"], lines[j][i + 1])

    # up
    for j in range(1, size_y):
        for i in range(size_x):
            max_to_side[j][i]["u"] = max(max_to_side[j - 1][i]["u"], lines[j - 1][i])

    # down
    for j in range(size_y - 2, -1, -1):
        for i in range(size_x):
            max_to_side[j][i]["d"] = max(max_to_side[j + 1][i]["d"], lines[j + 1][i])
    return max_to_side


def calculate_visibility(
    lines: list[list[int]], max_to_side: list[list[dict[str, int]]]
) -> list[list[int]]:
    size_x, size_y = len(max_to_side[0]), len(max_to_side)
    visibility = initialize_matrix(size_x, size_y, 1)

    for i in range(1, size_x - 1):
        for j in range(1, size_y - 1):
            visibility[j][i] = int(
                any(lines[j][i] > v for v in max_to_side[j][i].values())
            )

    return visibility


def calculate_one_view(lines: list[list[int]], x, y) -> int:
    size_x, size_y = len(lines[0]), len(lines)
    tree = lines[y][x]

    left = 0
    for i in range(x - 1, -1, -1):
        left += 1
        if lines[y][i] >= tree:
            break

    right = 0
    for i in range(x + 1, size_x):
        right += 1
        if lines[y][i] >= tree:
            break

    up = 0
    for j in range(y - 1, -1, -1):
        up += 1
        if lines[j][x] >= tree:
            break

    down = 0
    for j in range(y + 1, size_y):
        down += 1
        if lines[j][x] >= tree:
            break

    return left * right * up * down


def get_best_view(lines: list[list[int]], visibility: list[list[int]]) -> int:
    best_view = 0
    size_x, size_y = len(lines[0]), len(lines)
    for j in range(1, size_y - 1):
        for i in range(1, size_x - 1):
            if visibility[j][i]:
                best_view = max(calculate_one_view(lines, i, j), best_view)
    return best_view


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = convert(tokenize_by_char(reader.file_to_lines(8)), int)
    print_matrix(lines, limit=3)

    max_to_side = calculate_max_to_side(lines)
    print_matrix(max_to_side, limit=3)
    visibility = calculate_visibility(lines, max_to_side)
    print_matrix(visibility, limit=3)

    res_1 = sum(v for line in visibility for v in line)
    logger.info(f"{res_1=}...")

    res_2 = get_best_view(lines, visibility)
    logger.info(f"{res_2=}...")

    return res_1, res_2
