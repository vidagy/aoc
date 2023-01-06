import logging
from copy import deepcopy
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Reader:
    def __init__(self, year: int) -> None:
        self.year = year

    def get_input_path(self, task_num: int, sub_num: int = 0) -> str:
        filename = (
            f"task_{task_num:02d}" + (f"_{sub_num:02d}" if sub_num else "") + ".txt"
        )
        return str(
            Path(__file__).parent.parent.parent / "data" / str(self.year) / filename
        )

    def file_to_lines(self, task_num: int, sub_num: int = 0) -> list[str]:
        path = self.get_input_path(task_num, sub_num)
        res = []
        with open(path, "r") as f:
            logger.info(f"Reading file={path}")
            res = [line.strip("\n") for line in f.readlines()]
        logger.info(f"Read {len(res)} lines")
        return res


def split_lines_by_empty_line(inp: list[str]) -> list[list[str]]:
    res: list[list[str]] = []
    collector: list[str] = []
    for line in inp:
        if len(line.strip()) == 0:
            if collector:
                res.append(deepcopy(collector))
                collector = []
        else:
            collector.append(line)

    if collector:
        res.append(deepcopy(collector))
    return res


def tokenize(
    inp: list[str], separator: str = ",", skip_empty: bool = True
) -> list[list[str]]:
    out = []
    for line in inp:
        if skip_empty and not len(line.strip()):
            continue
        out.append([t.strip() for t in line.split(separator)])
    return out


def tokenize_by_char(inp: list[str], num=1, skip_empty: bool = True) -> list[list[str]]:
    out = []
    for line in inp:
        line_s = line.strip()
        if skip_empty and not len(line_s):
            continue
        collector = []
        for i in range(0, len(line_s), num):
            collector.append(line_s[i : i + num])
        out.append(collector)
    return out


def transpose(inp: list[list[str]]) -> list[list[str]]:
    assert len(inp) > 0
    col_num = len(inp[0])

    out: list[list[str]] = []
    for _ in range(col_num):
        out.append([])

    for i in range(len(inp)):
        for j in range(col_num):
            out[j].append(inp[i][j])

    return out


def convert(cols: list[list[str]], converter: Any) -> list[list[Any]]:
    # assert len(types) == len(cols)

    out = []

    for col in cols:
        new_col = []
        for row in col:
            new_col.append(converter(row))
        out.append(new_col)

    return out


def print_matrix(matrix: list[list[Any]], limit: int = 0, formatter="%s") -> None:
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return
    max_rows = limit if limit else len(matrix)
    for j in range(max_rows):
        max_cols = limit if limit else len(matrix[j])
        for i in range(max_cols):
            print(formatter % matrix[j][i], end=""),
        print()
    print()
