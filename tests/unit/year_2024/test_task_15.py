import logging

from aoc.year_2024.task_15 import MOVEMENTS, NarrowWarehouse, Pos, WideWarehouse

INP_SMALL = """
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########
"""

EXP_SMALL = """
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#O@..#
    #...O..#
    #...O..#
    ########
"""


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n") if line.strip()]


def test_move():
    w = NarrowWarehouse(get_lines(INP_SMALL))
    w.move(Pos(0, -1))
    assert w.map == NarrowWarehouse(get_lines(INP_SMALL)).map


def test_small():
    w = NarrowWarehouse(get_lines(INP_SMALL))
    movements = [MOVEMENTS[c] for c in "<^^>>>vv<v>>v<<"]
    for m in movements:
        logging.error(w)
        w.move(m)

    exp_w = NarrowWarehouse(get_lines(EXP_SMALL))
    assert exp_w.map == w.map
    assert w.gps_value() == 2028


INP_LARGE = """
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########
"""

INP_LARGE_WIDE = """
    ####################
    ##....[]....[]..[]##
    ##............[]..##
    ##..[][]....[]..[]##
    ##....[]@.....[]..##
    ##[]##....[]......##
    ##[]....[]....[]..##
    ##..[][]..[]..[][]##
    ##........[]......##
    ####################
"""

LARGE_MOVES = """<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

EXP_LARGE_WIDE = """
    ####################
    ##[].......[].[][]##
    ##[]...........[].##
    ##[]........[][][]##
    ##[]......[]....[]##
    ##..##......[]....##
    ##..[]............##
    ##..@......[].[][]##
    ##......[][]..[]..##
    ####################
"""


def test_transform():
    w = WideWarehouse(get_lines(INP_LARGE))
    w_exp = NarrowWarehouse(get_lines(INP_LARGE_WIDE))

    assert w.map == w_exp.map


def test_wide_large():
    w = WideWarehouse(get_lines(INP_LARGE))
    movements = [MOVEMENTS[c] for c in LARGE_MOVES]
    for m in movements:
        w.move(m)

    exp_w = NarrowWarehouse(get_lines(EXP_LARGE_WIDE))
    assert exp_w.map == w.map
    assert w.gps_value() == 9021


INP_SMALL_2 = """
    #######
    #...#.#
    #.....#
    #..OO@#
    #..O..#
    #.....#
    #######
"""

EXP_SMALL_2 = """
    ##############
    ##...[].##..##
    ##...@.[]...##
    ##....[]....##
    ##..........##
    ##..........##
    ##############
"""


def test_wide_small():
    w = WideWarehouse(get_lines(INP_SMALL_2))
    movements = [MOVEMENTS[c] for c in "<vv<<^^<<^^"]
    for m in movements:
        logging.error(w)
        w.move(m)

    exp_w = NarrowWarehouse(get_lines(EXP_SMALL_2))
    assert exp_w.map == w.map
