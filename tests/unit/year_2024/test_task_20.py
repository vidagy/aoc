from aoc.year_2024.task_20 import Maze


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n") if line.strip()]


INP = """
    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
"""


def test_find_itself():
    m = Maze.create(get_lines(INP))
    assert m.num_cheats_that_save_at_least_n(n=64) == 1
    assert m.num_cheats_that_save_at_least_n(n=40) == 2
    assert m.num_cheats_that_save_at_least_n(n=38) == 3
    assert m.num_cheats_that_save_at_least_n(n=36) == 4
    assert m.num_cheats_that_save_at_least_n(n=20) == 5
    assert m.num_cheats_that_save_at_least_n(n=12) == 8
