from aoc.registry import SolutionRegistry


def test_task_01():
    res_1, res_2 = SolutionRegistry.run(2024, 1)
    assert res_1 == 1660292
    assert res_2 == 22776016
