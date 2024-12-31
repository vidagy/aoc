from aoc.year_2024.task_17 import Computer


def test_find_itself():
    c = Computer(117440, 0, 0, [0, 3, 5, 4, 3, 0], 0, False, [])
    assert c.prints_itself()
