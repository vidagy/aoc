import logging
import re
from dataclasses import dataclass

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass
class Draw:
    red: int
    blue: int
    green: int

    @staticmethod
    def load(line: str) -> "Draw":
        def get_num_for(what: str) -> int:
            rex = re.compile(r"(\d+) " + what)
            match = rex.findall(line)
            return int(match[0]) if match else 0

        return Draw(
            get_num_for("red"),
            get_num_for("blue"),
            get_num_for("green"),
        )


@dataclass
class Game:
    id: int
    draws: list[Draw]

    @staticmethod
    def load(line: str) -> "Game":
        parts = line.split(":")
        id = int(parts[0].lower().strip("game "))
        draws = parts[1].split(";")

        return Game(id, [Draw.load(draw) for draw in draws])

    def power(self) -> int:
        r = max(d.red for d in self.draws)
        b = max(d.blue for d in self.draws)
        g = max(d.green for d in self.draws)

        return r * b * g


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(2)
    logger.info(f"{lines[:3]=}...")

    games = [Game.load(line) for line in lines]
    logger.info(f"{games[:3]=}...")

    res_1 = sum(
        game.id
        for game in games
        if all(
            draw.red <= 12 and draw.green <= 13 and draw.blue <= 14
            for draw in game.draws
        )
    )
    logger.info(f"{res_1=}")

    res_2 = sum(game.power() for game in games)
    logger.info(f"{res_2=}")

    return res_1, res_2
