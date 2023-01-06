import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, print_matrix, tokenize
from aoc.year_2022.task_08 import initialize_matrix

logger = logging.getLogger(__name__)


def get_register(lines: list[tuple[str, int]]) -> list[int]:
    current = 1
    register = [current]
    for (op, num) in lines:
        if op == "addx":
            register.append(current)
            register.append(current)
            current += num
        elif op == "noop":
            register.append(current)
        else:
            raise Exception(f"Not implemented {op=}")

    return register


def paint_screen(register: list[int]) -> list[list[str]]:
    screen: list[list[str]] = initialize_matrix(40, 6, ".")
    for pixel in range(240):
        j = pixel // 40
        i = pixel - (pixel // 40) * 40
        sprite_pos = register[pixel + 1]

        if abs(i - sprite_pos) <= 1:
            screen[j][i] = "#"

    return screen


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, list[list[str]]]:
    lines = tokenize(reader.file_to_lines(10), separator=" ")
    parsed_lines: list[tuple[str, int]] = [
        (line[0], int(line[1]) if len(line) == 2 else 0) for line in lines
    ]
    logger.info(f"{parsed_lines[:13]=}...")

    register = get_register(parsed_lines)
    logger.info(f"{len(register)=}: {register[:13]=}...")

    res_1 = (
        register[20] * 20
        + register[60] * 60
        + register[100] * 100
        + register[140] * 140
        + register[180] * 180
        + register[220] * 220
    )
    logger.info(f"{res_1=}")

    screen = paint_screen(register)
    print_matrix(screen)

    return res_1, screen
