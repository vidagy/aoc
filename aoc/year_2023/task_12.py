import logging
from dataclasses import dataclass

from cachetools import LRUCache, cachedmethod

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


OK = "."
MAYBE = "?"
BAD = "#"


@dataclass
class Row:
    data: str
    groups: tuple[int, ...]

    @staticmethod
    def create(line: str) -> "Row":
        data, groups = line.split()
        return Row(data, tuple(int(i) for i in groups.split(",")))

    def unfold(self) -> "Row":
        return Row(
            MAYBE.join([self.data] * 5),
            self.groups * 5,
        )


class ArrangementCounter:
    def __init__(self) -> None:
        self.cache: LRUCache = LRUCache(1024 * 1024)

    @staticmethod
    def _can_fit(data: str, groups: tuple[int, ...]) -> bool:
        looking_for = sum(groups)
        if looking_for > len(data.replace(".", "")):
            return False
        already_have = sum(1 for c in data if c == "#")
        if looking_for < already_have:
            return False

        return True

    @cachedmethod(lambda self: self.cache)
    def _count_arrangements_in(self, data: str, groups: tuple[int, ...]) -> int:
        if not data:
            # if there is no more string, then we can only fit zero groups in a single way
            return int(not groups)

        if not self._can_fit(data, groups):
            return 0

        if "." in data:
            # we can split it further
            i = data.find(".")
            head = data[:i]
            tail = data[i + 1 :]

            res = 0
            for j in range(len(groups) + 1):
                if self._can_fit(head, groups[:j]) and self._can_fit(tail, groups[j:]):
                    head_c = self._count_arrangements_in(head, groups[:j])
                    tail_c = self._count_arrangements_in(tail, groups[j:])
                    res += head_c * tail_c
            return res
        else:
            # there are no more dots, so the groups have to put them there
            if "?" in data:
                i = data.find("?")
                return self._count_arrangements_in(
                    data[:i] + "." + data[i + 1 :], groups
                ) + self._count_arrangements_in(data[:i] + "#" + data[i + 1 :], groups)
            else:
                # the only thing left is #
                return int(len(groups) == 1 and groups[0] == len(data))

    def __call__(self, row: Row) -> int:
        return self._count_arrangements_in(row.data, row.groups)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(12)
    logger.info(f"{lines[:3]=}...")

    rows = [Row.create(line) for line in lines]

    counter = ArrangementCounter()

    res_1 = sum(counter(row) for row in rows)
    logger.info(f"{res_1=}")

    rows = [row.unfold() for row in rows]

    res_2 = sum(counter(row) for row in rows)
    logger.info(f"{res_2=}")

    return res_1, res_2
