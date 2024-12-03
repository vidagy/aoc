import inspect
import re
from collections import defaultdict
from typing import Callable, Optional, TypeVar

from aoc.util.reader import Reader

T1 = TypeVar("T1")
T2 = TypeVar("T2")
SolveFunctionT = Callable[[Reader], tuple[T1, T2]]


class SolutionRegistry:
    solutions: dict[int, dict[int, SolveFunctionT]] = defaultdict(dict)

    @classmethod
    def get_year_date(
        cls, input_year: Optional[int], input_day: Optional[int]
    ) -> tuple[int, int]:
        y = input_year if input_year is not None else max(cls.solutions)
        d = input_day if input_day is not None else max(cls.solutions[y])
        return y, d

    @staticmethod
    def _get_year_day_of_this_solution() -> tuple[int, int]:
        # 2, because not this function (0),
        # not the register function (1),
        # but rather its call site: (2)
        solver_filename = inspect.stack()[2].filename
        rex = re.compile(r"year_([0-9]+).*task_([0-9]+)")
        year, day = rex.findall(solver_filename)[0]

        return int(year), int(day)

    @classmethod
    def register(cls, fun: SolveFunctionT) -> SolveFunctionT:
        year, day = cls._get_year_day_of_this_solution()
        cls.solutions[year][day] = fun

        return fun

    @classmethod
    def run(cls, year: int, day: int) -> tuple[T1, T2]:
        reader = Reader(year)
        return cls.solutions[year][day](reader)
