from aoc.year_2024.task_11 import evolve, len_evolve_n_times


def test_task_11():
    assert evolve(125) == (253000, None)
    assert evolve(17) == (1, 7)
    assert evolve(253000) == (253, 0)
    assert evolve(1) == (2024, None)
    assert evolve(7) == (14168, None)


def test_task_11_line():
    assert sum(len_evolve_n_times(n, 6) for n in [125, 17]) == 22
    assert sum(len_evolve_n_times(n, 25) for n in [125, 17]) == 55312
