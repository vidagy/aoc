import pytest

from aoc.registry import SolutionRegistry


def test_task_01():
    res_1, res_2 = SolutionRegistry.run(2022, 1)
    assert res_1 == 71471
    assert res_2 == 211189


def test_task_02():
    res_1, res_2 = SolutionRegistry.run(2022, 2)
    assert res_1 == 11767
    assert res_2 == 13886


def test_task_03():
    res_1, res_2 = SolutionRegistry.run(2022, 3)
    assert res_1 == 8053
    assert res_2 == 2425


def test_task_04():
    res_1, res_2 = SolutionRegistry.run(2022, 4)
    assert res_1 == 602
    assert res_2 == 891


def test_task_05():
    res_1, res_2 = SolutionRegistry.run(2022, 5)
    assert res_1 == "QMBMJDFTD"
    assert res_2 == "NBTVTJNFJ"


def test_task_06():
    res_1, res_2 = SolutionRegistry.run(2022, 6)
    assert res_1 == 1953
    assert res_2 == 2301


def test_task_07():
    res_1, res_2 = SolutionRegistry.run(2022, 7)
    assert res_1 == 1792222
    assert res_2 == 1112963


def test_task_08():
    res_1, res_2 = SolutionRegistry.run(2022, 8)
    assert res_1 == 1849
    assert res_2 == 201600


def test_task_09():
    res_1, res_2 = SolutionRegistry.run(2022, 9)
    assert res_1 == 6357
    assert res_2 == 2627


def test_task_10():
    res_1, res_2 = SolutionRegistry.run(2022, 10)
    assert res_1 == 13740
    task_10_res_2 = (
        "####.#..#.###..###..####.####..##..#....\n"
        "...#.#..#.#..#.#..#.#....#....#..#.#....\n"
        "..#..#..#.#..#.#..#.###..###..#....#....\n"
        ".#...#..#.###..###..#....#....#....#....\n"
        "#....#..#.#....#.#..#....#....#..#.#....\n"
        "####..##..#....#..#.#....####..##..####.\n"
    )
    assert res_2 == [[c for c in line] for line in task_10_res_2.split("\n") if line]


def test_task_11():
    res_1, res_2 = SolutionRegistry.run(2022, 11)
    assert res_1 == 113232
    assert res_2 == 29703395016


def test_task_12():
    res_1, res_2 = SolutionRegistry.run(2022, 12)
    assert res_1 == 456
    assert res_2 == 454


def test_task_13():
    res_1, res_2 = SolutionRegistry.run(2022, 13)
    assert res_1 == 6415
    assert res_2 == 20056


def test_task_14():
    res_1, res_2 = SolutionRegistry.run(2022, 14)
    assert res_1 == 625
    assert res_2 == 25193


@pytest.mark.slow
def test_task_15():
    res_1, res_2 = SolutionRegistry.run(2022, 15)
    assert res_1 == 4879972
    assert res_2 == 12525726647448


def test_task_16():
    res_1, res_2 = SolutionRegistry.run(2022, 16)
    assert res_1 == 1638
    assert res_2 == 0


def test_task_17():
    res_1, res_2 = SolutionRegistry.run(2022, 17)
    assert res_1 == 3206
    assert res_2 == 1602881844347


def test_task_18():
    res_1, res_2 = SolutionRegistry.run(2022, 18)
    assert res_1 == 3576
    assert res_2 == 2066


@pytest.mark.slow
def test_task_19():
    res_1, res_2 = SolutionRegistry.run(2022, 19)
    assert res_1 == 1418
    assert res_2 == 4114


@pytest.mark.slow
def test_task_20():
    res_1, res_2 = SolutionRegistry.run(2022, 20)
    assert res_1 == 1087
    assert res_2 == 13084440324666


def test_task_21():
    res_1, res_2 = SolutionRegistry.run(2022, 21)
    assert res_1 == 379578518396784
    assert res_2 == 3353687996514


def test_task_22():
    res_1, res_2 = SolutionRegistry.run(2022, 22)
    assert res_1 == 131052
    assert res_2 == 4578


@pytest.mark.slow
def test_task_23():
    res_1, res_2 = SolutionRegistry.run(2022, 23)
    assert res_1 == 3987
    assert res_2 == 938


@pytest.mark.slow
def test_task_24():
    res_1, res_2 = SolutionRegistry.run(2022, 24)
    assert res_1 == 260
    assert res_2 == 747


def test_task_25():
    res_1, res_2 = SolutionRegistry.run(2022, 25)
    assert res_1 == "2-==10===-12=2-1=-=0"
    assert res_2 == 0
