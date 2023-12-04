import logging
from dataclasses import dataclass

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass
class Card:
    id: int
    winning_numbers: set[int]
    my_numbers: set[int]
    num: int = 1

    @staticmethod
    def from_raw(line) -> "Card":
        id_part, num_part = line.split(":")
        id = int(id_part.split()[-1])

        winning_part, my_part = num_part.split("|")
        winning_numbers = set(int(num) for num in winning_part.split() if num != "")
        my_numbers = set(int(num) for num in my_part.split() if num != "")

        return Card(id, winning_numbers, my_numbers)

    @property
    def num_match(self):
        return len(self.winning_numbers.intersection(self.my_numbers))

    @property
    def points(self) -> int:
        return 2 ** (self.num_match - 1) if self.num_match > 0 else 0


def generate_cards(cards: list[Card]) -> None:
    for i, card in enumerate(cards):
        for j in range(i + 1, i + card.num_match + 1):
            cards[j].num += card.num


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(4)
    logger.info(f"{lines[:3]=}...")

    cards = [Card.from_raw(line) for line in lines]
    logger.info(f"{cards[:3]=}...")

    res_1 = sum(card.points for card in cards)
    logger.info(f"{res_1=}")

    generate_cards(cards)

    res_2 = sum(card.num for card in cards)
    logger.info(f"{res_2=}")

    return res_1, res_2
