import logging
from copy import deepcopy

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize

logger = logging.getLogger(__name__)


ROCK = 8
SAND = 0


def get_frame(lines: list[list[tuple[int, int]]]) -> tuple[int, int, int, int]:
    x_min = min(p[0] for line in lines for p in line)
    x_max = max(p[0] for line in lines for p in line)
    y_min = min(p[1] for line in lines for p in line)
    y_max = max(p[1] for line in lines for p in line)

    return x_min, x_max, y_min, y_max


def get_step(start: tuple[int, int], end: tuple[int, int]) -> tuple[int, int]:
    x_s, y_s = start
    x_e, y_e = end

    s_x, s_y = 0, 0
    if x_s != x_e:
        s_x = (x_e - x_s) // abs(x_e - x_s)
    if y_s != y_e:
        s_y = (y_e - y_s) // abs(y_e - y_s)

    return s_x, s_y


def add_line(canvas: dict[tuple[int, int], int], line: list[tuple[int, int]]) -> None:
    start = line[0]
    for end in line[1:]:
        step = get_step(start, end)

        current = start
        while current != end:
            canvas[current] = ROCK
            current = (current[0] + step[0], current[1] + step[1])

        canvas[current] = ROCK

        start = end


def get_canvas(lines: list[list[tuple[int, int]]]) -> dict[tuple[int, int], int]:
    canvas: dict[tuple[int, int], int] = {}
    for line in lines:
        add_line(canvas, line)
    return canvas


def fall_one_step(
    canvas: dict[tuple[int, int], int], y_max: int, pos: tuple[int, int]
) -> tuple[tuple[int, int], bool, bool]:
    falls_to_death = pos[1] + 1 > y_max

    # down
    if (pos[0], pos[1] + 1) not in canvas:
        # it can free fall
        return (pos[0], pos[1] + 1), True, falls_to_death
    elif (pos[0] - 1, pos[1] + 1) not in canvas:
        # it can left
        return (pos[0] - 1, pos[1] + 1), True, falls_to_death
    elif (pos[0] + 1, pos[1] + 1) not in canvas:
        # it can right
        return (pos[0] + 1, pos[1] + 1), True, falls_to_death
    else:
        return pos, False, falls_to_death


def add_one_sand_grain(canvas: dict[tuple[int, int], int], y_max: int) -> bool:
    pos: tuple[int, int] = (500, 0)

    can_move = True
    falls_to_death = False

    if pos in canvas:
        return True

    while can_move and not falls_to_death:
        pos, can_move, falls_to_death = fall_one_step(canvas, y_max, pos)

    if not falls_to_death:
        canvas[pos] = SAND

    return falls_to_death


def fill_with_sand(canvas: dict[tuple[int, int], int], y_max: int) -> None:
    falls_to_death = False
    while not falls_to_death:
        falls_to_death = add_one_sand_grain(canvas, y_max)


def add_base_floor(canvas: dict[tuple[int, int], int], y_max: int) -> None:
    y = y_max + 2
    x_min = 500 - y - 2
    x_max = 500 + y + 2
    line = [(x_min, y), (x_max, y)]
    add_line(canvas, line)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = tokenize(reader.file_to_lines(14), separator="->")
    raw_lines = [convert(tokenize(line), int) for line in inp]
    lines: list[list[tuple[int, int]]] = [
        [tuple(p) for p in line] for line in raw_lines  # type: ignore
    ]
    logger.info(f"{lines[:3]=}")

    x_min, x_max, y_min, y_max = get_frame(lines)
    logger.info(f"{x_min=} {x_max=} {y_min=} {y_max=}")

    canvas = get_canvas(lines)
    canvas_2 = deepcopy(canvas)
    # logger.info(f"{canvas.items()=}")

    fill_with_sand(canvas, y_max)
    res_1 = sum(1 for _, v in canvas.items() if v == SAND)
    logger.info(f"{res_1=}")

    add_base_floor(canvas_2, y_max)
    fill_with_sand(canvas_2, y_max + 5)
    res_2 = sum(1 for _, v in canvas_2.items() if v == SAND)
    logger.info(f"{res_2=}")

    return res_1, res_2
