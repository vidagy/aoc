from aoc.year_2023.task_10 import Pipes, count_containment


def util(input: str, expected: int, expected_area: int) -> None:
    lines = [line.strip() for line in input.split("\n") if line.strip()]
    pipes = Pipes.create(lines)

    s_pipe, path = pipes.find_steps(lines)
    assert (len(path) + 2) // 2 == expected

    lines[pipes.start.x] = (
        lines[pipes.start.x][: pipes.start.y]
        + s_pipe
        + lines[pipes.start.x][pipes.start.y + 1 :]
    )
    path.append(pipes.start)
    assert count_containment(path, lines) == expected_area


def test_simple():
    INPUT = """
        .....
        .S-7.
        .|.|.
        .L-J.
        .....
    """
    util(INPUT, 4, 1)


def test_simple_with_noise():
    INPUT = """
        -L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF
    """
    util(INPUT, 4, 1)


def test_complicated():
    INPUT = """
        ..F7.
        .FJ|.
        SJ.L7
        |F--J
        LJ...
    """
    util(INPUT, 8, 1)


def test_complicated_with_noise():
    INPUT = """
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
    """
    util(INPUT, 8, 1)


def test_simple_large():
    INPUT = """
        ...........
        .S-------7.
        .|F-----7|.
        .||.....||.
        .||.....||.
        .|L-7.F-J|.
        .|..|.|..|.
        .L--J.L--J.
        ...........
    """
    util(INPUT, 23, 4)


def test_complicated_large():
    INPUT = """
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
    """
    util(INPUT, 70, 8)


def test_complicated_large_with_noise():
    INPUT = """
        FF7FSF7F7F7F7F7F---7
        L|LJ||||||||||||F--J
        FL-7LJLJ||||||LJL-77
        F--JF--7||LJLJ7F7FJ-
        L---JF-JLJ.||-FJLJJ7
        |F|F-JF---7F7-L7L|7|
        |FFJF7L7F-JF7|JL---7
        7-L-JL7||F7|L7F-7F7|
        L.L7LFJ|||||FJL7||LJ
        L7JLJL-JLJLJL--JLJ.L
    """
    util(INPUT, 80, 10)
