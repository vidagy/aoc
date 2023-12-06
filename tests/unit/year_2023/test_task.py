from aoc.registry import SolutionRegistry


def test_task_01():
    res_1, res_2 = SolutionRegistry.run(2023, 1)
    assert res_1 == 54940
    assert res_2 == 54208


def test_task_02():
    res_1, res_2 = SolutionRegistry.run(2023, 2)
    assert res_1 == 2076
    assert res_2 == 70950


def test_task_03():
    res_1, res_2 = SolutionRegistry.run(2023, 3)
    assert res_1 == 546563
    assert res_2 == 91031374


def test_task_04():
    res_1, res_2 = SolutionRegistry.run(2023, 4)
    assert res_1 == 20117
    assert res_2 == 13768818


def test_task_05():
    res_1, res_2 = SolutionRegistry.run(2023, 5)
    assert res_1 == 525792406
    assert res_2 == 79004094


def test_task_06():
    res_1, res_2 = SolutionRegistry.run(2023, 6)
    assert res_1 == 1159152
    assert res_2 == 41513103
