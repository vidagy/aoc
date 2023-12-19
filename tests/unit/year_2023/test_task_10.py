from aoc.year_2023.task_10 import Pipes


def util(input: str, expected: int) -> None:
    lines = [line.strip() for line in input.split("\n") if line.strip()]
    pipes = Pipes.create(lines)

    path = pipes.find_steps(lines)
    assert (len(path) + 2) // 2 == expected


def test_simple():
    INPUT = """
        .....
        .S-7.
        .|.|.
        .L-J.
        .....
    """
    util(INPUT, 4)


def test_simple_with_noise():
    INPUT = """
        -L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF
    """
    util(INPUT, 4)


def test_complicated():
    INPUT = """
        ..F7.
        .FJ|.
        SJ.L7
        |F--J
        LJ...
    """
    util(INPUT, 8)


def test_complicated_with_noise():
    INPUT = """
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
    """
    util(INPUT, 8)
