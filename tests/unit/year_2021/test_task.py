from aoc.registry import SolutionRegistry


def test_task_01():
    res_1, res_2 = SolutionRegistry.run(2021, 1)
    assert res_1 == 1451
    assert res_2 == 1395


def test_task_02():
    res_1, res_2 = SolutionRegistry.run(2021, 2)
    assert res_1 == 1714680
    assert res_2 == 1963088820


def test_task_03():
    res_1, res_2 = SolutionRegistry.run(2021, 3)
    assert res_1 == 3882564
    assert res_2 == 3385170


def test_task_04():
    res_1, res_2 = SolutionRegistry.run(2021, 4)
    assert res_1 == 4662
    assert res_2 == 12080
