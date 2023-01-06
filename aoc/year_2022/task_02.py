import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize

logger = logging.getLogger(__name__)

ROCK = "A"
PAPER = "B"
SCISSORS = "C"


def what_beats_this(this: str):
    if this == ROCK:
        return PAPER
    if this == PAPER:
        return SCISSORS
    if this == SCISSORS:
        return ROCK


def this_beats_what(this: str):
    if this == ROCK:
        return SCISSORS
    if this == PAPER:
        return ROCK
    if this == SCISSORS:
        return PAPER


value_mapping = {
    PAPER: 2,
    SCISSORS: 3,
    ROCK: 1,
}


def value_of_match(their: str, mine_input: str) -> int:
    winning_mapping = {
        "Y": PAPER,
        "X": ROCK,
        "Z": SCISSORS,
    }
    mine = winning_mapping[mine_input]

    res = value_mapping[mine]
    if their == what_beats_this(mine):
        return res
    if their == mine:
        return res + 3
    if what_beats_this(their) == mine:
        return res + 6

    raise Exception("Logic Error")


def value_of_match_part_2(their: str, outcome: str) -> int:
    outcome_point_mapping = {
        "X": 0,
        "Y": 3,
        "Z": 6,
    }
    if outcome == "X":
        mine = this_beats_what(their)
    if outcome == "Y":
        mine = their
    if outcome == "Z":
        mine = what_beats_this(their)

    return outcome_point_mapping[outcome] + value_mapping[mine]


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = tokenize(reader.file_to_lines(2), separator=" ")
    logger.info(f"{lines[:3]=}...")

    all_points = sum(value_of_match(f, s) for [f, s] in lines)
    logger.info(f"{all_points=}")

    all_points_2 = sum(value_of_match_part_2(f, s) for [f, s] in lines)
    logger.info(f"{all_points_2=}")

    return all_points, all_points_2
