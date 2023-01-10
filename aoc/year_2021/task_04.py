import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


class Bingo:
    def __init__(self, rows: list[str]) -> None:
        if len(rows) != 5:
            raise Exception("Cannot parse")
        self.board: list[list[int]] = []
        for row in rows:
            self.board.append([int(x) for x in row.split()])

    def __repr__(self) -> str:
        res = ""
        for row in self.board:
            for num in row:
                res += f"{num:3d}"
            res += "\n"
        return res

    def check(self, draws: set[int]) -> bool:
        for row in self.board:
            if all(n in draws for n in row):
                return True

        for col_i in range(len(self.board[0])):
            if all(r[col_i] in draws for r in self.board):
                return True

        return False


def parse(lines: list[str]) -> tuple[list[int], list[Bingo]]:
    groups = split_lines_by_empty_line(lines)
    draws = [int(n) for n in groups[0][0].split(",")]
    bingos = [Bingo(rows) for rows in groups[1:]]

    return draws, bingos


def get_first_winner(
    draws: list[int], boards: list[Bingo]
) -> tuple[int, set[int], Bingo]:
    draws_so_far = set()

    for num in draws:
        draws_so_far.add(num)
        for bingo in boards:
            if bingo.check(draws_so_far):
                return num, draws_so_far, bingo

    raise Exception("No solution")


def get_last_winner(
    draws: list[int], boards: list[Bingo]
) -> tuple[int, set[int], Bingo]:
    draws_so_far = set()
    last_winner = None

    for num in draws:
        draws_so_far.add(num)
        not_winners = []
        for bingo in boards:
            if not bingo.check(draws_so_far):
                not_winners.append(bingo)

        if len(not_winners) == 1:
            last_winner = not_winners[0]
        if len(not_winners) == 0:
            if last_winner is None:
                raise Exception("No solution")
            return num, draws_so_far, last_winner

    raise Exception("No solution")


def get_res(i: int, draws: set[int], board: Bingo) -> int:
    logger.info(f"{i=}")
    s = sum(n for row in board.board for n in row if n not in draws)
    logger.info(f"{s=}")
    return i * s


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(4)
    draws, boards = parse(inp)
    # logger.info(f"{draws[:3]=}...")
    # logger.info(f"{boards[:3]=}...")

    i, draws_so_far, bingo = get_first_winner(draws, boards)
    res_1 = get_res(i, draws_so_far, bingo)
    logger.info(f"{res_1=}")

    i2, draws_so_far2, bingo2 = get_last_winner(draws, boards)
    res_2 = get_res(i2, draws_so_far2, bingo2)
    logger.info(f"{res_2=}")

    return res_1, res_2
