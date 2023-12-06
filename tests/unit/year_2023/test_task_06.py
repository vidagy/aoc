from aoc.year_2023.task_06 import Race

INPUT = """Time:      7  15   30
Distance:  9  40  200"""


def test_part_1():
    raw_time, raw_dist = [line.strip() for line in INPUT.split("\n")]
    races = Race.load(raw_time, raw_dist)

    for race in races:
        assert race.count_that_beats() == race.count_that_beats_2()
