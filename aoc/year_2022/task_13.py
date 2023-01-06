import logging
from enum import Enum
from functools import cmp_to_key
from typing import Union

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, split_lines_by_empty_line

logger = logging.getLogger(__name__)


T = Union[list["T"], int]


class CmpRes(Enum):
    Less = -1
    Eq = 0
    Greater = 1


def compare_int(left: int, right: int) -> CmpRes:
    return (
        CmpRes.Less if left < right else CmpRes.Eq if left == right else CmpRes.Greater
    )


def compare_list(left: list[T], right: list[T]) -> CmpRes:
    s_left = len(left)
    s_right = len(right)

    for i in range(min(s_left, s_right)):
        left_e = left[i]
        right_e = right[i]
        cmp_res = compare_T(left_e, right_e)
        if cmp_res != CmpRes.Eq:
            return cmp_res

    if s_left < s_right:
        return CmpRes.Less
    elif s_left > s_right:
        return CmpRes.Greater

    return CmpRes.Eq


def compare_T(left: T, right: T) -> CmpRes:
    if isinstance(left, int) and isinstance(right, int):
        return compare_int(left, right)
    elif isinstance(left, list) and isinstance(right, list):
        return compare_list(left, right)
    elif isinstance(left, int) and isinstance(right, list):
        return compare_list([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare_list(left, [right])
    else:
        raise Exception("Cannot be")


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(13)
    lines = convert(split_lines_by_empty_line(inp), converter=eval)
    logger.info(f"{len(lines)=}")

    in_order = [
        i
        for (i, row) in enumerate(lines, start=1)
        if compare_T(row[0], row[1]) != CmpRes.Greater
    ]
    res_1 = sum(in_order)
    logger.info(f"{res_1=}")

    all_lines = [line for two_line in lines for line in two_line]

    all_lines.append([[2]])
    all_lines.append([[6]])

    def cmp(left: T, right: T) -> int:
        return compare_T(left, right).value

    all_lines = sorted(all_lines, key=cmp_to_key(cmp))
    first_pos = [
        i
        for i, elem in enumerate(all_lines, start=1)
        if compare_T(elem, [[2]]) == CmpRes.Eq
    ][0]
    second_pos = [
        i
        for i, elem in enumerate(all_lines, start=1)
        if compare_T(elem, [[6]]) == CmpRes.Eq
    ][0]

    res_2 = first_pos * second_pos
    logger.info(f"{res_2=}")

    return res_1, res_2
