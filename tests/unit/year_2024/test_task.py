from aoc.registry import SolutionRegistry


def test_task_01():
    res_1, res_2 = SolutionRegistry.run(2024, 1)
    assert res_1 == 1660292
    assert res_2 == 22776016


def test_task_02():
    res_1, res_2 = SolutionRegistry.run(2024, 2)
    assert res_1 == 213
    assert res_2 == 285


def test_task_03():
    res_1, res_2 = SolutionRegistry.run(2024, 3)
    assert res_1 == 187825547
    assert res_2 == 85508223


def test_task_04():
    res_1, res_2 = SolutionRegistry.run(2024, 4)
    assert res_1 == 2603
    assert res_2 == 1965


def test_task_05():
    res_1, res_2 = SolutionRegistry.run(2024, 5)
    assert res_1 == 4814
    assert res_2 == 5448
