import logging
import re
from dataclasses import dataclass
from typing import Optional

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


@dataclass
class Game:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    @staticmethod
    def create(raw_game: list[str]) -> "Game":
        assert len(raw_game) == 3
        button_a = tuple(int(n) for n in re.findall(r"(\d+)", raw_game[0]))
        button_b = tuple(int(n) for n in re.findall(r"(\d+)", raw_game[1]))
        prize = tuple(int(n) for n in re.findall(r"(\d+)", raw_game[2]))
        return Game(button_a, button_b, prize)  # type: ignore

    def cost(self) -> Optional[int]:
        t_11 = self.button_b[1]
        t_12 = -1 * self.button_b[0]
        t_21 = -1 * self.button_a[1]
        t_22 = self.button_a[0]

        d = self.button_a[0] * self.button_b[1] - self.button_b[0] * self.button_a[1]

        a_num = self.prize[0] * t_11 + self.prize[1] * t_12
        b_num = self.prize[0] * t_21 + self.prize[1] * t_22

        if (a_num % d) or (b_num % d):
            return None

        return 3 * (a_num // d) + (b_num // d)

    def move_price(self) -> "Game":
        return Game(
            self.button_a,
            self.button_b,
            (self.prize[0] + 10000000000000, self.prize[1] + 10000000000000),
        )


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_games = split_lines_by_empty_line(reader.file_to_lines(13))
    games = [Game.create(g) for g in raw_games]
    logger.info(f"{games[:3]=}...")

    res_1 = sum(game.cost() or 0 for game in games)
    logger.info(f"{res_1=}")

    res_2 = sum(game.move_price().cost() or 0 for game in games)
    logger.info(f"{res_2=}")

    return res_1, res_2
