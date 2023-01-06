import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)

ROW = {(3, 0), (4, 0), (5, 0), (6, 0)}
CROSS = {(3, 1), (4, 0), (4, 1), (4, 2), (5, 1)}
ANGLE = {(3, 0), (4, 0), (5, 0), (5, 1), (5, 2)}
BAR = {(3, 0), (3, 1), (3, 2), (3, 3)}
BOX = {(3, 0), (3, 1), (4, 0), (4, 1)}

SHAPES = [ROW, CROSS, ANGLE, BAR, BOX]


def get_empty_canvas() -> list[list[bool]]:
    canvas: list[list[bool]] = []

    canvas.append([True for _ in range(10)])
    for i in range(7):
        canvas.append([False for _ in range(10)])
    canvas.append([True for _ in range(10)])

    for column in canvas:
        column[0] = True

    return canvas


def get_shape(round: int, current_level: int) -> list[tuple[int, int]]:
    shape = SHAPES[round % len(SHAPES)]
    return [(x, y + current_level + 3 + 1) for x, y in shape]


def get_current_level(shape: list[tuple[int, int]], current_level: int) -> int:
    level = max([current_level] + [y for _, y in shape])
    # logger.info(f"{level=}")
    return level


def move_jets(
    shape: list[tuple[int, int]],
    canvas: list[list[bool]],
    jets: list[tuple[int, int]],
    vertical_time: int,
) -> tuple[bool, list[tuple[int, int]]]:
    movement = jets[vertical_time % len(jets)]
    new_shape = [(x + movement[0], y + movement[1]) for x, y in shape]
    can_move = not any(canvas[x][y] for x, y in new_shape)

    if can_move:
        # logger.info(f" -> Moving to {movement=}, {new_shape=}")
        return True, new_shape
    else:
        # logger.info(f" -> Could not move jet")
        return False, shape


def move_down(
    shape: list[tuple[int, int]], canvas: list[list[bool]]
) -> tuple[bool, list[tuple[int, int]]]:
    new_shape = [(x, y - 1) for x, y in shape]
    can_move = not any(canvas[x][y] for x, y in new_shape)
    if can_move:
        # logger.info(f" -> Moving to (0, -1), {new_shape=}")
        return True, new_shape
    else:
        # logger.info(f" -> Could not move jet")
        return False, shape


def move_while_can(
    shape: list[tuple[int, int]],
    canvas: list[list[bool]],
    jets: list[tuple[int, int]],
    vertical_time: int,
    current_level: int,
) -> tuple[list[tuple[int, int]], int, int]:
    while True:
        could_move, shape = move_jets(shape, canvas, jets, vertical_time)
        vertical_time += 1

        could_move, shape = move_down(shape, canvas)
        if not could_move:
            break

    return shape, vertical_time, get_current_level(shape, current_level)


def add_to_canvas(
    canvas: list[list[bool]], shape: list[tuple[int, int]]
) -> list[list[bool]]:
    for x, y in shape:
        canvas[x][y] = True
    return canvas


def extend_canvas(canvas: list[list[bool]], current_level: int) -> list[list[bool]]:
    # logger.info("Extending canvas")
    for i, column in enumerate(canvas):
        while len(column) < current_level + 10:
            column.append(i == 0 or i == 8)
    return canvas


def play(
    canvas: list[list[bool]], jets: list[tuple[int, int]], rounds: int
) -> list[int]:
    current_level = 0
    vertical_time = 0

    levels: list[int] = [0]

    for round in range(rounds):
        shape = get_shape(round, current_level)
        # logger.info(f"{round:4d} NEW SHAPE: {current_level=} {shape=}")
        shape, vertical_time, current_level = move_while_can(
            shape, canvas, jets, vertical_time, current_level
        )
        canvas = add_to_canvas(canvas, shape)
        canvas = extend_canvas(canvas, current_level)

        levels.append(current_level)

        # print_canvas(canvas)

    return levels


def print_canvas(canvas: list[list[bool]]) -> None:
    logger.info("")
    logger.info("".join(["-" for _ in canvas[0]]))
    for row in canvas[1:-1]:
        logger.info("".join(["#" if x else " " for x in row]))
    logger.info("".join(["-" for _ in canvas[0]]))
    logger.info("")


def find_cycle(nums: list[int]) -> list[int]:
    cycle = [nums[0]]
    while True:
        good = True
        for i in range(len(nums) - len(cycle)):
            j = i + len(cycle)
            if nums[i] != nums[j]:
                cycle.append(nums[len(cycle)])
                good = False
                break
        if good:
            break
    logger.info(f"Found {len(cycle)=} {cycle[:15]=}...")
    return cycle


def extrapolate_level(levels: list[int], at: int) -> int:
    if at < len(levels) // 5:
        return levels[at]

    diffs = [levels[i + 1] - levels[i] for i in range(0, len(levels) - 1)]

    cycle_start = len(levels) // 5
    mid_section = diffs[cycle_start:-cycle_start]
    cycle = find_cycle(mid_section)

    cycle_diff = sum(cycle)

    read_at = at - cycle_start
    return (
        levels[cycle_start]
        + (read_at // len(cycle)) * cycle_diff
        + sum(cycle[0 : (read_at % len(cycle))])
    )


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(17)[0].strip()
    # inp = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    logger.info(f"{inp[:3]=}...")
    jets = [(-1, 0) if c == "<" else (1, 0) for c in inp]

    canvas = get_empty_canvas()
    levels = play(canvas, jets, rounds=100000)

    res_1 = levels[2022]
    res_2 = extrapolate_level(levels, 1000000000000)
    logger.info(f"{res_1=}")
    logger.info(f"{res_2=}")

    return res_1, res_2
