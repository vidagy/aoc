from aoc.year_2024.task_12 import count_borders_x, count_intervals


def test_count_intervals():
    assert count_intervals({}) == 0
    assert count_intervals({1}) == 1
    assert count_intervals({1, 2}) == 1
    assert count_intervals({1, 2, 3}) == 1
    assert count_intervals({1, 3}) == 2
    assert count_intervals({1, 2, 4}) == 2
    assert count_intervals({1, 3, 4}) == 2
    assert count_intervals({1, 2, 4, 5}) == 2
    assert count_intervals({1, 2, 4, 6, 7, 8, 9, 11}) == 4
