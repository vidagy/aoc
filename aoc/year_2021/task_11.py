import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize_by_char

logger = logging.getLogger(__name__)


def get_neighbors(x: int, y: int, width: int, height: int) -> list[tuple[int, int]]:
    x_n = [xx for xx in [x + 1, x, x - 1] if 0 <= xx < width]
    y_n = [yy for yy in [y + 1, y, y - 1] if 0 <= yy < height]
    res = []
    for xx in x_n:
        for yy in y_n:
            if not (xx == x and yy == y):
                res.append((xx, yy))
    return res


def increase_all_by_one(board: list[list[int]]) -> set[tuple[int, int]]:
    height = len(board)
    width = len(board[0])

    res = set()

    for i in range(width):
        for j in range(height):
            board[j][i] += 1
            if board[j][i] == 10:
                res.add((i, j))

    return res


def reset_board(board: list[list[int]]):
    height = len(board)
    width = len(board[0])

    for i in range(width):
        for j in range(height):
            if board[j][i] > 9:
                board[j][i] = 0


def evolve(i, board: list[list[int]]) -> int:
    height = len(board)
    width = len(board[0])

    already_blinked = set()
    to_visit = set(increase_all_by_one(board))

    while to_visit:
        xx, yy = to_visit.pop()
        if (xx, yy) in already_blinked:
            continue
        already_blinked.add((xx, yy))
        n = get_neighbors(xx, yy, width, height)
        for xxx, yyy in n:
            board[yyy][xxx] += 1
            if board[yyy][xxx] == 10:
                to_visit.add((xxx, yyy))
        already_blinked.add((xx, yy))

    reset_board(board)
    return len(already_blinked)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    board = convert(tokenize_by_char(reader.file_to_lines(11)), int)
    logger.info(f"{board=}")

    res_1 = 0
    for i in range(100):
        res_1 += evolve(i, board)
    logger.info(f"{res_1=}")

    res_2 = 100
    while True:
        blinks = evolve(res_2, board)
        res_2 += 1
        if blinks == len(board) * len(board[0]):
            break
    logger.info(f"{res_2=}")

    return res_1, res_2
