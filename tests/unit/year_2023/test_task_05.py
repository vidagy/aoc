from aoc.year_2023.task_05 import TaskInput, get_seed_to_location

INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test_part_1():
    lines = [line.strip() for line in INPUT.split("\n")]

    task_input = TaskInput.read(lines)
    seed_to_location = get_seed_to_location(task_input)
    res_1 = min(seed_to_location.values())

    assert res_1 == 35

    res_2 = task_input.get_min_location_for_seed_ranges()
    assert res_2 == 46
