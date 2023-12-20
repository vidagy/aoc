import logging
from dataclasses import dataclass
from typing import Callable, Optional

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


@dataclass
class Cluster:
    data: list[list[bool]]

    @staticmethod
    def create(lines: list[str]) -> "Cluster":
        data: list[list[bool]] = []
        for line in lines:
            data.append([])
            for c in line:
                data[-1].append(c == "#")
        return Cluster(data)

    def value(self, expected_difference: int = 0) -> int:
        return (self.find_vertical_reflection(expected_difference) or 0) + (
            self.find_horizontal_reflection(expected_difference) or 0
        ) * 100

    @property
    def row_getter(self) -> Callable[[int], list[bool]]:
        def _getter(i: int) -> list[bool]:
            return self.data[i]

        return _getter

    @property
    def col_getter(self) -> Callable[[int], list[bool]]:
        def _getter(i: int) -> list[bool]:
            return [line[i] for line in self.data]

        return _getter

    def _find_reflections(
        self, getter: Callable[[int], list[bool]], width: int, expected_difference: int
    ) -> Optional[int]:
        reflections = set()
        for centerline in range(1, width):
            differences = 0
            for delta in range(1, width):
                lower = centerline - delta
                upper = centerline + delta - 1
                if lower < 0 or upper >= width:
                    continue
                differences += sum(
                    lle != ule for lle, ule in zip(getter(lower), getter(upper))
                )
                if differences > expected_difference:
                    break
            if differences == expected_difference:
                reflections.add(centerline)
        if len(reflections) == 1:
            return next(iter(reflections))
        elif len(reflections) > 1:
            raise Exception("Too many reflections")
        return None

    def find_horizontal_reflection(self, expected_difference: int = 0) -> Optional[int]:
        return self._find_reflections(
            self.row_getter, len(self.col_getter(0)), expected_difference
        )

    def find_vertical_reflection(self, expected_difference: int = 0) -> Optional[int]:
        return self._find_reflections(
            self.col_getter, len(self.row_getter(0)), expected_difference
        )


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    line_clusters = split_lines_by_empty_line(reader.file_to_lines(13))
    # logger.info(f"{lines[:3]=}...")
    clusters = [Cluster.create(lines) for lines in line_clusters]

    res_1 = sum(c.value() for c in clusters)
    logger.info(f"{res_1=}")

    res_2 = sum(c.value(expected_difference=1) for c in clusters)
    logger.info(f"{res_2=}")

    return res_1, res_2
