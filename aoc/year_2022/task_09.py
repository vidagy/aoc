import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize, transpose

logger = logging.getLogger(__name__)


DIR_DIFF_MAP = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def get_head_path(steps: list[tuple[str, int]]) -> list[tuple[int, int]]:
    current_pos = (0, 0)
    path = [current_pos]

    for step in steps:
        direction, count = step
        for i in range(count):
            current_pos = (
                current_pos[0] + DIR_DIFF_MAP[direction][0],
                current_pos[1] + DIR_DIFF_MAP[direction][1],
            )
            path.append(current_pos)
    return path


def is_too_far(x: tuple[int, int], y: tuple[int, int]) -> bool:
    return abs(x[0] - y[0]) > 1 or abs(x[1] - y[1]) > 1


def step(tail: tuple[int, int], head: tuple[int, int]) -> tuple[int, int]:
    if not is_too_far(head, tail):
        return tail

    x_diff = head[0] - tail[0]
    y_diff = head[1] - tail[1]

    if x_diff == 0:
        return (tail[0], tail[1] + y_diff // abs(y_diff))
    if y_diff == 0:
        return (tail[0] + x_diff // abs(x_diff), tail[1])

    x_step = x_diff // abs(x_diff)
    y_step = y_diff // abs(y_diff)

    return (tail[0] + x_step, tail[1] + y_step)


def get_tail_path(head_path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    current_pos = (0, 0)
    path = [current_pos]
    for head_pos in head_path[1:]:
        current_pos = step(current_pos, head_pos)
        path.append(current_pos)
    return path


def step_rope(rope_pos: list[tuple[int, int]], head_pos: tuple[int, int]) -> None:
    pre = head_pos
    for i in range(len(rope_pos)):
        rope_pos[i] = step(rope_pos[i], pre)
        pre = rope_pos[i]
    return


def get_rope_tail_path(
    head_path: list[tuple[int, int]], rope_length: int
) -> list[tuple[int, int]]:
    rope_pos = [(0, 0) for i in range(rope_length)]
    path = [(0, 0)]

    for head_pos in head_path[1:]:
        step_rope(rope_pos, head_pos)
        # logger.info(
        #     f"{head_pos=} -> {rope_pos=}"
        # )
        path.append(rope_pos[-1])

    return path


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = tokenize(reader.file_to_lines(9), separator=" ")
    logger.info(f"{lines[:3]=}...")

    cols = transpose(lines)
    cols[1] = [int(i) for i in cols[1]]  # type: ignore
    lines = transpose(cols)
    logger.info(f"{lines[:8]=}...")

    head_path = get_head_path(lines)  # type: ignore
    logger.info(f"{head_path[:18]=}...")
    tail_path = get_tail_path(head_path)
    logger.info(f"{tail_path[:18]=}...")

    res_1 = len(set(tail_path))
    logger.info(f"{res_1=}")

    rope_tail_path = get_rope_tail_path(head_path, 9)
    logger.info(f"{rope_tail_path[:18]=}...")
    res_2 = len(set(rope_tail_path))
    logger.info(f"{res_2=}")

    return res_1, res_2
