import pytest

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


@pytest.mark.slow
def test_task_06():
    res_1, res_2 = SolutionRegistry.run(2024, 6)
    assert res_1 == 5461
    assert res_2 == 1836


def test_task_07():
    res_1, res_2 = SolutionRegistry.run(2024, 7)
    assert res_1 == 5512534574980
    assert res_2 == 328790210468594


def test_task_08():
    res_1, res_2 = SolutionRegistry.run(2024, 8)
    assert res_1 == 367
    assert res_2 == 1285


@pytest.mark.slow
def test_task_09():
    res_1, res_2 = SolutionRegistry.run(2024, 9)
    assert res_1 == 6288707484810
    assert res_2 == 6311837662089
