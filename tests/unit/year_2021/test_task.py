from aoc.registry import SolutionRegistry


def test_task_01():
    res_1, res_2 = SolutionRegistry.run(2021, 1)
    assert res_1 == 1451
    assert res_2 == 1395


def test_task_02():
    res_1, res_2 = SolutionRegistry.run(2021, 2)
    assert res_1 == 1714680
    assert res_2 == 1963088820
