from aoc.year_2024.task_04 import DiagonalIterator, count_words


def test_diagonal_iter():
    inp = [[1, 2, 3], [4, 5, 6]]

    assert [line for line in DiagonalIterator(inp)] == [[1], [4, 2], [5, 3], [6]]


def get_lines(inp: str) -> list[list[str]]:
    return [line.strip() for line in inp.split("\n") if line.strip()]


def test_small():
    INP = get_lines(
        """
        ..X...
        .SAMX.
        .A..A.
        XMAS.S
        .X....
    """
    )

    assert count_words(INP) == 4


def test_larger():
    INP = get_lines(
        """
            MMMSXXMASM
            MSAMXMSMSA
            AMXSXMAAMM
            MSAMASMSMX
            XMASAMXAMM
            XXAMMXXAMA
            SMSMSASXSS
            SAXAMASAAA
            MAMMMXMMMM
            MXMXAXMASX
        """
    )
    assert count_words(INP) == 18
