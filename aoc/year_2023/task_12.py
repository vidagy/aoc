import logging
from dataclasses import dataclass
from itertools import zip_longest

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


OK = "."
MAYBE = "?"
BAD = "#"


@dataclass
class Row:
    data: str
    groups: list[int]

    @staticmethod
    def create(line: str) -> "Row":
        data, groups = line.split()
        return Row(data, [int(i) for i in groups.split(",")])

    def num_arrangements(self) -> int:
        return Row.num_arrangement_of("", self.data, self.groups)

    def unfold(self) -> "Row":
        return Row(
            MAYBE.join([self.data, self.data, self.data, self.data, self.data]),
            [*self.groups, *self.groups, *self.groups, *self.groups, *self.groups],
        )

    @staticmethod
    def extract_groups(data: str) -> list[int]:
        g = []
        current = 0
        for c in data:
            if c == BAD:
                current += 1
            else:
                if current:
                    g.append(current)
                    current = 0
        if current:
            g.append(current)
        return g

    @staticmethod
    def match_groups(data: str, groups: list[int]) -> bool:
        return Row.extract_groups(data) == groups

    @staticmethod
    def num_arrangement_of(fix: str, variable: str, groups: list[int]) -> int:
        full = fix + variable
        finished = not variable or not any(c == MAYBE for c in variable)
        if finished:
            return Row.match_groups(full, groups)

        count_bads = sum(c == BAD for c in full)
        count_maybe = sum(c == MAYBE for c in full)

        count_bad_needed = sum(groups)

        if count_bads > count_bad_needed:
            return 0
        if count_bads + count_maybe < count_bad_needed:
            return 0

        current_groups = Row.extract_groups(fix)
        if len(current_groups) > len(groups):
            return 0
        if len(current_groups):
            for current_group, expected_group in zip_longest(
                current_groups[:-1], groups
            ):
                if current_group and current_group != expected_group:
                    return 0
            if current_groups[-1] > groups[len(current_groups) - 1]:
                return 0

        i = variable.find(MAYBE)
        new_fix = fix + variable[:i]
        new_variable = variable[i + 1 :]
        return Row.num_arrangement_of(
            new_fix + OK, new_variable, groups
        ) + Row.num_arrangement_of(new_fix + BAD, new_variable, groups)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(12)
    logger.info(f"{lines[:3]=}...")

    rows = [Row.create(line) for line in lines]

    res_1 = sum(row.num_arrangements() for row in rows)
    logger.info(f"{res_1=}")

    rows = [row.unfold() for row in rows]
    res_2 = 0
    # for i, row in enumerate(rows):
    #     logger.info(f"{i=}")
    #     res_2 += row.num_arrangements()
    # logger.info(f"{res_2=}")

    return res_1, res_2
