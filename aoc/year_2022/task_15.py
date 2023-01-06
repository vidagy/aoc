import logging
from typing import Optional

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def distance(s_x: int, s_y: int, b_x: int, b_y: int) -> int:
    return abs(s_x - b_x) + abs(s_y - b_y)


def process_line(line: str) -> tuple[int, int, int, int]:
    sensor, beacon = line.split(":")
    first, second = sensor.split(",")
    s_x = int(first.split("=")[1])
    s_y = int(second.split("=")[1])

    first, second = beacon.split(",")
    b_x = int(first.split("=")[1])
    b_y = int(second.split("=")[1])

    return s_x, s_y, b_x, b_y


def get_frame(lines: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    x_min = min(p for line in lines for p in [line[0], line[2]])
    x_max = max(p for line in lines for p in [line[0], line[2]])
    y_min = min(p for line in lines for p in [line[1], line[3]])
    y_max = max(p for line in lines for p in [line[1], line[3]])

    # adjust with distance

    for line in lines:
        s_x, s_y, b_x, b_y = line
        d = distance(s_x, s_y, b_x, b_y)
        x_min = min(x_min, s_x - d)
        x_max = max(x_max, s_x + d)
        y_min = min(y_min, s_y - d)
        y_max = max(y_max, s_y + d)

    return x_min, x_max, y_min, y_max


def cannot_be(
    y: int, lines: list[tuple[int, int, int, int]], x_min: int, x_max: int
) -> int:
    is_covered: set[int] = set()

    for line in lines:
        s_x, s_y, b_x, b_y = line
        d = distance(s_x, s_y, b_x, b_y)

        d_y = abs(y - s_y)
        if d_y > d:
            continue

        d_x = d - d_y

        x_min = s_x - d_x
        x_max = s_x + d_x

        for x in range(x_min, x_max + 1):
            if not (b_y == y and x == b_x):
                is_covered.add(x)

    return len(is_covered)


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort()
    stack = []
    stack.append(intervals[0])
    for i in intervals[1:]:
        if stack[-1][0] <= i[0] <= stack[-1][-1] + 1:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)

    return stack


def missig_elem(
    intervals: list[list[int]], limit: int, y: int
) -> Optional[tuple[int, int]]:
    if len(intervals) == 1:
        if intervals[0][0] != 0:
            logger.info(f"got it {intervals[0][0]=} {y=}")
            return intervals[0][0], y
        elif intervals[0][1] != limit:
            logger.info(f"got it {intervals[0][1]=} {y=}")
            return intervals[0][1], y
        return None
    elif len(intervals) == 2:
        logger.info(f"got it {intervals[0][0] + 1=} {y=}")
        return intervals[0][1] + 1, y
    else:
        return None


def can_be(lines: list[tuple[int, int, int, int]], limit: int) -> tuple[int, int]:
    rows: list[list[list[int]]] = []
    for _ in range(limit + 1):
        rows.append([])

    for line in lines:
        s_x, s_y, b_x, b_y = line
        d = distance(s_x, s_y, b_x, b_y)

        logger.info(f"{s_x=} {s_y=} {b_x=} {b_y=} {d=}")

        for d_y in range(-d, d + 1):
            d_x = d - abs(d_y)

            x_min = s_x - d_x
            x_max = s_x + d_x

            y = s_y + d_y
            if 0 <= y <= limit and (x_min <= limit or x_max >= 0):
                # logger.info(f" --> add range {y=} {x_min=} {x_max=}")
                rows[y].append([max(0, x_min), min(limit, x_max)])

    logger.info("Checking rows...")

    for y, row in enumerate(rows):
        # logger.info(f" -> {row=}")
        intervals = merge_intervals(row)
        # logger.info(f"{y=} {intervals=}")
        missing = missig_elem(intervals, limit, y)
        if missing:
            return missing

    raise Exception("no solution")


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(15)
    lines = [process_line(line) for line in inp]
    logger.info(f"{lines[:3]=}")

    x_min, x_max, y_min, y_max = get_frame(lines)
    logger.info(f"{x_min=} {x_max=} {y_min=} {y_max=}")

    res_1 = cannot_be(2000000, lines, x_min, x_max)
    logger.info(f"{res_1=}")

    point = can_be(lines, 4000000)
    res_2 = 4000000 * point[0] + point[1]
    logger.info(f"{res_2=}")

    return res_1, res_2
