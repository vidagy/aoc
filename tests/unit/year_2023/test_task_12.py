from aoc.year_2023.task_12 import ArrangementCounter, Row

INPUT = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_1():
    assert ArrangementCounter()(Row.create("???.### 1,1,3")) == 1


def test_2():
    assert ArrangementCounter()(Row.create(".??..??...?##. 1,1,3")) == 4


def test_3():
    assert ArrangementCounter()(Row.create("?#?#?#?#?#?#?#? 1,3,1,6")) == 1


def test_4():
    assert ArrangementCounter()(Row.create("????.#...#... 4,1,1")) == 1


def test_5():
    assert ArrangementCounter()(Row.create("????.######..#####. 1,6,5")) == 4


def test_6():
    assert ArrangementCounter()(Row.create("?###???????? 3,2,1")) == 10


def test_1_2():
    assert ArrangementCounter()(Row.create("???.### 1,1,3").unfold()) == 1


def test_2_2():
    assert ArrangementCounter()(Row.create(".??..??...?##. 1,1,3").unfold()) == 16384


def test_3_2():
    assert ArrangementCounter()(Row.create("?#?#?#?#?#?#?#? 1,3,1,6").unfold()) == 1


def test_4_2():
    assert ArrangementCounter()(Row.create("????.#...#... 4,1,1").unfold()) == 16


def test_5_2():
    assert (
        ArrangementCounter()(Row.create("????.######..#####. 1,6,5").unfold()) == 2500
    )


def test_6_2():
    assert ArrangementCounter()(Row.create("?###???????? 3,2,1").unfold()) == 506250
