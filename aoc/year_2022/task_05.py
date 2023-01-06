import logging
from collections import defaultdict
from copy import deepcopy

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


def parse_stacks(lines: list[str]) -> list[list[str]]:
    max_length = max(len(line) for line in lines)
    num_of_cols = (max_length + 1) // 4
    logger.info(f"{num_of_cols=}...")
    cols = defaultdict(list)
    for line in lines[::-1][1:]:
        logger.info(f"{line=}...")
        for i in range(num_of_cols):
            char = line[1 + 4 * i]
            if char.isalpha():
                cols[i].append(char)
    logger.info(f"{cols=}...")
    return [cols[i] for i in range(len(cols))]


def parse_moves(lines: list[str]) -> list[tuple[int, int, int]]:
    moves: list[tuple[int, int, int]] = []
    for line in lines:
        moves.append(
            tuple(
                int(num)
                for num in line.replace("move", "")
                .replace("from", "")
                .replace("to", "")
                .strip()
                .split()
            )  # type: ignore
        )
    logger.info(f"{moves[:3]=}...")
    return moves


def apply_move(stacks: list[list[str]], num: int, from_stack: int, to_stack: int):
    for _ in range(num):
        stacks[to_stack - 1].append(stacks[from_stack - 1].pop())


def apply_move_2(stacks: list[list[str]], num: int, from_stack: int, to_stack: int):
    for i in range(-num, 0):
        stacks[to_stack - 1].append(stacks[from_stack - 1].pop(i))


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[str, str]:
    lines = split_lines_by_empty_line(reader.file_to_lines(5))
    raw_stacks = lines[0]
    logger.info(f"{raw_stacks[:]=}...")
    stacks = parse_stacks(raw_stacks)
    stacks_2 = deepcopy(stacks)

    raw_moves = lines[1]
    logger.info(f"{raw_moves[:3]=}...")
    moves = parse_moves(raw_moves)

    for move in moves:
        apply_move(stacks, *move)

    logger.info(f"{stacks=}")

    res_1 = "".join([stacks[i][-1] for i in range(len(stacks))])
    logger.info(f"{res_1=}")

    #

    for move in moves:
        apply_move_2(stacks_2, *move)

    logger.info(f"{stacks_2=}")

    res_2 = "".join([stacks_2[i][-1] for i in range(len(stacks_2))])
    logger.info(f"{res_2=}")

    return res_1, res_2
