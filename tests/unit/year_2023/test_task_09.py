from aoc.year_2023.task_09 import Sequence

INPUT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_get_next_and_prev():
    lines = [line.strip() for line in INPUT.split("\n")]
    seqs = [Sequence.create(line) for line in lines]

    assert seqs[0].get_next() == 18
    assert seqs[1].get_next() == 28
    assert seqs[2].get_next() == 68

    assert seqs[0].get_prev() == -3
    assert seqs[1].get_prev() == 0
    assert seqs[2].get_prev() == 5
