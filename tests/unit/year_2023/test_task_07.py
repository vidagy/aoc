from aoc.year_2023.task_07 import Bet, Hand, get_bet_ranks

INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_part_1():
    lines = [line.strip() for line in INPUT.split("\n")]
    bets = [Bet.crate(line) for line in lines]
    sorted_bets = sorted(bets)
    assert ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"] == [
        bet.hand.cards for bet in sorted_bets
    ]
    res_1 = get_bet_ranks(bets)
    assert res_1 == 6440


def test_compare():
    assert Hand("33332") > Hand("2AAAA")
    assert Hand("77888") > Hand("77788")
