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


def test_task_05():
    res_1, res_2 = SolutionRegistry.run(2021, 5)
    assert res_1 == 6856
    assert res_2 == 20666


def test_task_06():
    res_1, res_2 = SolutionRegistry.run(2021, 6)
    assert res_1 == 361169
    assert res_2 == 1634946868992


def test_task_07():
    res_1, res_2 = SolutionRegistry.run(2021, 7)
    assert res_1 == 336120
    assert res_2 == 96864235


def test_task_08():
    res_1, res_2 = SolutionRegistry.run(2021, 8)
    assert res_1 == 519
    assert res_2 == 1027483


def test_task_09():
    res_1, res_2 = SolutionRegistry.run(2021, 9)
    assert res_1 == 558
    assert res_2 == 882942


def test_task_10():
    res_1, res_2 = SolutionRegistry.run(2021, 10)
    assert res_1 == 278475
    assert res_2 == 3015539998


def test_task_11():
    res_1, res_2 = SolutionRegistry.run(2021, 11)
    assert res_1 == 1608
    assert res_2 == 214


def test_task_12():
    res_1, res_2 = SolutionRegistry.run(2021, 12)
    assert res_1 == 4338
    assert res_2 == 114189


def test_task_13():
    res_1, res_2 = SolutionRegistry.run(2021, 13)
    assert res_1 == 631
    assert res_2 == (
        "#### #### #    ####   ##  ##  ###  ####\n"
        "#    #    #    #       # #  # #  # #   \n"
        "###  ###  #    ###     # #    #  # ### \n"
        "#    #    #    #       # # ## ###  #   \n"
        "#    #    #    #    #  # #  # # #  #   \n"
        "#### #    #### #     ##   ### #  # #   \n"
    )
