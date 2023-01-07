import inspect
import re
from collections import defaultdict
from typing import Callable, Optional, TypeVar

from aoc.util.reader import Reader

T1 = TypeVar("T1")
T2 = TypeVar("T2")
SolveFunctionT = Callable[[Reader], tuple[T1, T2]]


def run(year: Optional[int], day: Optional[int]) -> tuple[T1, T2]:
    return SolutionRegistry.run(year, day)


class SolutionRegistry:
    solutions: dict[int, dict[int, SolveFunctionT]] = defaultdict(dict)

    @staticmethod
    def get_year_day() -> tuple[int, int]:
        # 2, because not this function (0),
        # not the register function (1),
        # but rather its call site: (2)
        solver_filename = inspect.stack()[2].filename
        rex = re.compile(r"year_([0-9]+).*task_([0-9]+)")
        year, day = rex.findall(solver_filename)[0]

        return int(year), int(day)

    @classmethod
    def register(cls, fun: SolveFunctionT) -> SolveFunctionT:
        year, day = cls.get_year_day()
        cls.solutions[year][day] = fun

        return fun

    @classmethod
    def run(cls, year: Optional[int], day: Optional[int]) -> tuple[T1, T2]:
        y = year if year is not None else max(cls.solutions)
        d = day if day is not None else max(cls.solutions[y])

        reader = Reader(y)
        return cls.solutions[y][d](reader)
