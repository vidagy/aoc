from aoc.year_2024.task_14 import Floor, Robot


def test_robot():
    robot = Robot(2, 4, 2, -3)
    robot.evolve(1, 11, 7)
    assert (4, 1) == (robot.x, robot.y)
    robot.evolve(1, 11, 7)
    assert (6, 5) == (robot.x, robot.y)
    robot.evolve(1, 11, 7)
    assert (8, 2) == (robot.x, robot.y)
    robot.evolve(1, 11, 7)
    assert (10, 6) == (robot.x, robot.y)


INP = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n") if line.strip()]


def test_floor():
    floor = Floor(get_lines(INP), 11, 7)

    floor.evolve(100)
    poss = [(robot.x, robot.y) for robot in floor.robots]
    poss.sort()
    assert poss == [
        (0, 2),
        (1, 3),
        (1, 6),
        (2, 3),
        (3, 5),
        (4, 5),
        (4, 5),
        (5, 4),
        (6, 0),
        (6, 0),
        (6, 6),
        (9, 0),
    ]

    assert floor.safety_factor() == 12
