from aoc.year_2023.task_13 import Cluster

INPUT_1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.""".split()


def test_1():
    cluster = Cluster.create(INPUT_1)
    assert cluster.find_horizontal_reflection() is None
    assert cluster.find_vertical_reflection() == 5
    assert cluster.value() == 5

    assert cluster.find_horizontal_reflection(1) == 3
    assert cluster.find_vertical_reflection(1) is None
    assert cluster.value(1) == 300


INPUT_2 = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split()


def test_2():
    cluster = Cluster.create(INPUT_2)
    assert cluster.find_horizontal_reflection() == 4
    assert cluster.find_vertical_reflection() is None
    assert cluster.value() == 400

    assert cluster.find_horizontal_reflection(1) == 1
    assert cluster.find_vertical_reflection(1) is None
    assert cluster.value(1) == 100


INPUT_3 = """..#....
...#.#.
###.###
###.###
...#.#.
..#....
.#.###.
#.....#
#.#...#
.#.###.
..#....
...#.#.
###.###""".split()


def test_3():
    cluster = Cluster.create(INPUT_3)
    assert cluster.find_horizontal_reflection() == 3
    assert cluster.find_vertical_reflection() is None
    assert cluster.value() == 300


INPUT_4 = """
###.###..#....#..
#....#.#.#.#####.
#.#....#.....###.
.###.##..######.#
.....#....#.##.##
.....#....#.##.##
.###.##..######.#
#.#....#.....###.
##...#.#.#.#####.
###.###..#....#..
....#...#.#......
..##.##.#.###.#..
..##.##.#.###.#..
""".split()


def test_4():
    cluster = Cluster.create(INPUT_4)
    assert cluster.find_horizontal_reflection() == 12
    assert cluster.find_vertical_reflection() is None
    assert cluster.value() == 1200
