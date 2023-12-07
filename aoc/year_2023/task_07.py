import logging
from collections import Counter
from dataclasses import dataclass
from enum import Enum

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FLUSH = 7


CARD_VALUES = {
    "*": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass
class Hand:
    cards: str

    def __post_init__(self):
        self.hand_type = Hand.get_hand_type(self.cards)

    @staticmethod
    def get_hand_type(cards: str) -> HandType:
        if len(cards) != 5:
            raise Exception(f"Whaaaat? {cards=}")

        temp = cards.replace("*", "")
        counts = sorted(list(Counter(temp).values()))
        if not counts:
            counts = [5]
        else:
            counts[-1] += cards.count("*")

        if counts == [5]:
            return HandType.FLUSH
        if counts == [1, 4]:
            return HandType.FOUR_OF_A_KIND
        if counts == [2, 3]:
            return HandType.FULL_HOUSE
        if counts == [1, 1, 3]:
            return HandType.THREE_OF_A_KIND
        if counts == [1, 2, 2]:
            return HandType.TWO_PAIRS
        if counts == [1, 1, 1, 2]:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    def __lt__(self, other: "Hand") -> bool:
        if self.hand_type != other.hand_type:
            return self.hand_type.value < other.hand_type.value
        for i in range(5):
            if self.cards[i] != other.cards[i]:
                return CARD_VALUES[self.cards[i]] < CARD_VALUES[other.cards[i]]
        raise Exception(f"equal {self=} {other=}")


@dataclass
class Bet:
    hand: Hand
    bid: int

    @staticmethod
    def crate(line: str) -> "Bet":
        cards, bid = line.split()
        return Bet(Hand(cards), int(bid))

    def __lt__(self, other: "Bet") -> bool:
        if self.hand.cards == other.hand.cards:
            raise Exception("same hands")
        return self.hand < other.hand

    def __eq__(self, other) -> bool:
        return self.hand.cards == other.hand.cards and self.bid == other.bid

    def __repr__(self) -> str:
        return f"{self.hand}: {self.bid}"


def get_bet_ranks(bets: list[Bet]) -> int:
    sorted_bets = sorted(bets)
    logger.info(f"{sorted_bets[:3]=}...")
    return sum(rank * hand.bid for rank, hand in enumerate(sorted_bets, start=1))


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(7)
    logger.info(f"{lines[:3]=}...")

    bets = [Bet.crate(line) for line in lines]

    res_1 = get_bet_ranks(bets)
    logger.info(f"{res_1=}")

    joker_bets = [Bet(Hand(b.hand.cards.replace("J", "*")), b.bid) for b in bets]

    res_2 = get_bet_ranks(joker_bets)
    logger.info(f"{res_2=}")

    return res_1, res_2
