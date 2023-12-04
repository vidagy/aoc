from aoc.year_2023.task_03 import Num, get_nums_next_to_symbols

INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_part_1():
    lines = [line.strip() for line in INPUT.split("\n") if line]

    n_x = len(lines)
    n_y = len(lines[0])

    nums = [
        num for n, line in enumerate(lines) for num in Num.extract_from_line(n, line)
    ]
    nums_next_to_symbols = get_nums_next_to_symbols(n_x, n_y, nums, lines)
    res_1 = sum(n.val for n in nums_next_to_symbols)
    assert res_1 == 4361
