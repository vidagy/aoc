from aoc.year_2024.task_05 import get_order_and_updates, is_update_ordered, order_line

INP = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n")]


def test_task_05():
    order, updates = get_order_and_updates(get_lines(INP))

    assert is_update_ordered(updates[0], order)
    assert is_update_ordered(updates[1], order)
    assert is_update_ordered(updates[2], order)
    assert not is_update_ordered(updates[3], order)
    assert not is_update_ordered(updates[4], order)
    assert not is_update_ordered(updates[5], order)

    assert 143 == sum(
        line[len(line) // 2] for line in updates if is_update_ordered(line, order)
    )

    assert order_line(updates[3], order) == [97, 75, 47, 61, 53]
    assert order_line(updates[4], order) == [61, 29, 13]
    assert order_line(updates[5], order) == [97, 75, 47, 29, 13]

    assert 123 == sum(
        order_line(line, order)[len(line) // 2]
        for line in updates
        if not is_update_ordered(line, order)
    )
