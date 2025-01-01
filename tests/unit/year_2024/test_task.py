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


def test_task_10():
    res_1, res_2 = SolutionRegistry.run(2024, 10)
    assert res_1 == 778
    assert res_2 == 1925


def test_task_11():
    res_1, res_2 = SolutionRegistry.run(2024, 11)
    assert res_1 == 235850
    assert res_2 == 279903140844645


def test_task_12():
    res_1, res_2 = SolutionRegistry.run(2024, 12)
    assert res_1 == 1451030
    assert res_2 == 859494


def test_task_13():
    res_1, res_2 = SolutionRegistry.run(2024, 13)
    assert res_1 == 27105
    assert res_2 == 101726882250942


@pytest.mark.slow
def test_task_14():
    res_1, res_2 = SolutionRegistry.run(2024, 14)
    assert res_1 == 224438715
    assert res_2 == 7603


def test_task_15():
    res_1, res_2 = SolutionRegistry.run(2024, 15)
    assert res_1 == 1526673
    assert res_2 == 1535509


def test_task_16():
    res_1, res_2 = SolutionRegistry.run(2024, 16)
    assert res_1 == 89460
    assert res_2 == 504


def test_task_17():
    res_1, res_2 = SolutionRegistry.run(2024, 17)
    assert res_1 == "6,7,5,2,1,3,5,1,7"
    assert res_2 == 0


def test_task_18():
    res_1, res_2 = SolutionRegistry.run(2024, 18)
    assert res_1 == 404
    assert res_2 == "27,60"


def test_task_19():
    res_1, res_2 = SolutionRegistry.run(2024, 19)
    assert res_1 == 272
    assert res_2 == 1041529704688380


@pytest.mark.slow
def test_task_20():
    res_1, res_2 = SolutionRegistry.run(2024, 20)
    assert res_1 == 1351
    assert res_2 == 966130
