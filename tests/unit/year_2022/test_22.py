from aoc.util.reader import Reader
from aoc.year_2022.task_22 import DOWN, LEFT, RIGHT, UP, Plan2, Walk, parse_input_2


def get_test_plan() -> Plan2:
    inp = Reader(2022).file_to_lines(22)
    new_inp = []
    for line in inp:
        new_inp.append(line.replace("#", "."))
    plan, _ = parse_input_2(new_inp)
    return plan


def test_22_rounds():
    plan = get_test_plan()
    S = plan.size
    for dir in [LEFT, RIGHT, UP, DOWN]:
        for current_pos in [
            (S, 0),
            (S, S - 1),
            (S, S),
            (2 * S - 1, S),
            (2 * S - 1, 2 * S - 1),
            (S, 2 * S - 1),
            (S - 1, 3 * S - 1),
            (S - 1, 3 * S),
            (S, 3 * S - 1),
        ]:
            plan.direction = dir
            plan.pos = current_pos

            instruction = Walk(1)
            for i in range(4 * plan.size):
                instruction.do(plan)

            assert plan.direction == dir
            assert plan.pos == current_pos
