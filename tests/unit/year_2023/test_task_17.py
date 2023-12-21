from aoc.year_2023.task_17 import UltraCrucibleMap

INPUT = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".split()


def test_task_17():
    assert 102 == UltraCrucibleMap(INPUT, 1, 3).shortest_weights()
    assert 94 == UltraCrucibleMap(INPUT, 4, 10).shortest_weights()


INPUT_2 = """111111111111
999999999991
999999999991
999999999991
999999999991""".split()


def test_task_17_2():
    assert 71 == UltraCrucibleMap(INPUT_2, 4, 10).shortest_weights()
