import logging
from typing import Generic, Iterator, TypeVar

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, rotate, transpose

logger = logging.getLogger(__name__)


def count_words_in_row(line: list[str]) -> int:
    res = 0

    if len(line) < 4:
        return res

    for i in range(len(line) - 3):
        if "".join(line[i : i + 4]) == "XMAS":
            res += 1

    return res


T = TypeVar("T")


class DiagonalIterator(Iterator, Generic[T]):
    def __init__(self, inp: list[list[T]]) -> None:
        self.inp = inp
        self.offset = 0
        self.n_x = len(inp)
        self.n_y = len(inp[0])

    def __iter__(self) -> "DiagonalIterator":
        return self

    def __next__(self) -> list[T]:
        if self.offset >= self.n_x + self.n_y - 1:
            raise StopIteration

        line = []

        x = self.offset if self.offset < self.n_x else self.n_x - 1
        y = 0 if self.offset < self.n_x else self.offset - self.n_x + 1

        while x >= 0 and y < self.n_y:
            line.append(self.inp[x][y])
            x -= 1
            y += 1

        self.offset += 1

        return line


def count_words(lines: list[list[str]]) -> int:
    res = 0

    res += sum(count_words_in_row(line) for line in lines)
    res += sum(count_words_in_row(line[::-1]) for line in lines)

    transposed = transpose(lines)
    res += sum(count_words_in_row(line) for line in transposed)
    res += sum(count_words_in_row(line[::-1]) for line in transposed)

    res += sum(count_words_in_row(line) for line in DiagonalIterator(lines))
    res += sum(count_words_in_row(line[::-1]) for line in DiagonalIterator(lines))

    rotated = rotate(lines)
    res += sum(count_words_in_row(line) for line in DiagonalIterator(rotated))
    res += sum(count_words_in_row(line[::-1]) for line in DiagonalIterator(rotated))

    return res


def is_x_mas(lines: list[str], x: int, y: int) -> bool:
    d_1 = "".join([lines[x - 1][y - 1], lines[x][y], lines[x + 1][y + 1]])
    d_2 = "".join([lines[x - 1][y + 1], lines[x][y], lines[x + 1][y - 1]])

    def is_diagonal_mas(d: str) -> bool:
        return d == "MAS" or d == "SAM"

    return is_diagonal_mas(d_1) and is_diagonal_mas(d_2)


def count_mas(lines) -> int:
    res = 0
    for x in range(1, len(lines) - 1):
        for y in range(1, len(lines[0]) - 1):
            if is_x_mas(lines, x, y):
                res += 1
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(4)
    logger.info(f"{lines[:3]=}...")

    res_1 = count_words([list(line) for line in lines])
    logger.info(f"{res_1=}")

    res_2 = count_mas(lines)
    logger.info(f"{res_2=}")

    return res_1, res_2
