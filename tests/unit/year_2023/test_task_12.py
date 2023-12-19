from aoc.year_2023.task_12 import Row

INPUT = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_1():
    assert Row.create("???.### 1,1,3").num_arrangements() == 1


def test_2():
    assert Row.create(".??..??...?##. 1,1,3").num_arrangements() == 4


def test_3():
    assert Row.create("?#?#?#?#?#?#?#? 1,3,1,6").num_arrangements() == 1


def test_4():
    assert Row.create("????.#...#... 4,1,1").num_arrangements() == 1


def test_5():
    assert Row.create("????.######..#####. 1,6,5").num_arrangements() == 4


def test_6():
    assert Row.create("?###???????? 3,2,1").num_arrangements() == 10


def test_1_2():
    assert Row.create("???.### 1,1,3").unfold().num_arrangements() == 1


def test_2_2():
    assert Row.create(".??..??...?##. 1,1,3").unfold().num_arrangements() == 16384


def test_3_2():
    assert Row.create("?#?#?#?#?#?#?#? 1,3,1,6").unfold().num_arrangements() == 1


def test_4_2():
    assert Row.create("????.#...#... 4,1,1").unfold().num_arrangements() == 16


def test_5_2():
    assert Row.create("????.######..#####. 1,6,5").unfold().num_arrangements() == 2500


def test_6_2():
    assert Row.create("?###???????? 3,2,1").unfold().num_arrangements() == 506250
