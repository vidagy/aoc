from aoc.year_2024.task_07 import Expression


def test_task_07():
    assert Expression("190: 10 19").possible()
    assert Expression("3267: 81 40 27").possible()
    assert not Expression("83: 17 5").possible()
    assert not Expression("156: 15 6").possible()
    assert not Expression("7290: 6 8 6 15").possible()
    assert not Expression("161011: 16 10 13").possible()
    assert not Expression("192: 17 8 14").possible()
    assert not Expression("21037: 9 7 18 13").possible()
    assert Expression("292: 11 6 16 20").possible()

    assert Expression("190: 10 19").possible(with_concatenation=True)
    assert Expression("3267: 81 40 27").possible(with_concatenation=True)
    assert not Expression("83: 17 5").possible(with_concatenation=True)
    assert Expression("156: 15 6").possible(with_concatenation=True)
    assert Expression("7290: 6 8 6 15").possible(with_concatenation=True)
    assert not Expression("161011: 16 10 13").possible(with_concatenation=True)
    assert Expression("192: 17 8 14").possible(with_concatenation=True)
    assert not Expression("21037: 9 7 18 13").possible(with_concatenation=True)
    assert Expression("292: 11 6 16 20").possible(with_concatenation=True)
