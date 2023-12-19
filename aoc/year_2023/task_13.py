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

    def value(self) -> int:
        return (self.find_vertical_reflection() or 0) + (
            self.find_horizontal_reflection() or 0
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
        self, getter: Callable[[int], list[bool]], width: int
    ) -> Optional[int]:
        candidates = set()
        anti_candidates = set()

        for i in range(width - 1):
            col = getter(i)
            for j in range(i + 1, width):
                other_col = getter(j)
                if col == other_col:
                    if (j - i) % 2 != 0:
                        val = (j + i + 1) // 2
                        if val not in anti_candidates:
                            candidates.add(val)
                else:
                    if (j - i) % 2 != 0:
                        val = (j + i + 1) // 2
                        anti_candidates.add(val)
        candidates = candidates.difference(anti_candidates)
        if len(candidates) == 1:
            return next(iter(candidates))
        elif len(candidates) > 1:
            raise Exception("fuck!")
        return None

    def find_horizontal_reflection(self) -> Optional[int]:
        return self._find_reflections(self.row_getter, width=len(self.col_getter(0)))

    def find_vertical_reflection(self) -> Optional[int]:
        return self._find_reflections(self.col_getter, width=len(self.row_getter(0)))


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    line_clusters = split_lines_by_empty_line(reader.file_to_lines(13))
    # logger.info(f"{lines[:3]=}...")
    clusters = [Cluster.create(lines) for lines in line_clusters]

    res_1 = sum(c.value() for c in clusters)
    logger.info(f"{res_1=}")

    res_2 = 0
    logger.info(f"{res_2=}")

    return res_1, res_2
