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


def test_task_07():
    res_1, res_2 = SolutionRegistry.run(2023, 7)
    assert res_1 == 246795406
    assert res_2 == 249356515


def test_task_08():
    res_1, res_2 = SolutionRegistry.run(2023, 8)
    assert res_1 == 20659
    assert res_2 == 15690466351717


def test_task_09():
    res_1, res_2 = SolutionRegistry.run(2023, 9)
    assert res_1 == 1868368343
    assert res_2 == 1022


def test_task_10():
    res_1, res_2 = SolutionRegistry.run(2023, 10)
    assert res_1 == 0
    assert res_2 == 0


def test_task_11():
    res_1, res_2 = SolutionRegistry.run(2023, 11)
    assert res_1 == 10173804
    assert res_2 == 634324905172
