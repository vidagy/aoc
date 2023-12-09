import logging
from copy import deepcopy
from dataclasses import dataclass
from itertools import islice, tee

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def is_all_zero(nums: list[int]) -> bool:
    return all(num == 0 for num in nums)


def get_diffs(nums: list[int]) -> list[int]:
    if len(nums) < 2:
        raise Exception("too short")

    these, nexts = tee(nums, 2)
    nexts = islice(nexts, 1, None)
    return [n - c for c, n in zip(these, nexts)]


@dataclass
class Sequence:
    nums: list[int]

    def __post_init__(self):
        diffs = get_diffs(self.nums)
        self.mmap = [deepcopy(self.nums), diffs]
        while not is_all_zero(diffs):
            diffs = get_diffs(diffs)
            self.mmap.append(diffs)

    @staticmethod
    def create(raw: str) -> "Sequence":
        return Sequence([int(n) for n in raw.split()])

    def get_next(self) -> int:
        prevs, these = tee(self.mmap[::-1], 2)
        these = islice(these, 1, None)

        for prev, this in zip(prevs, these):
            this.append(this[-1] + prev[-1])

        return self.mmap[0][-1]

    def get_prev(self) -> int:
        prevs, these = tee(self.mmap[::-1], 2)
        these = islice(these, 1, None)

        for prev, this in zip(prevs, these):
            this.insert(0, this[0] - prev[0])

        return self.mmap[0][0]


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(9)

    seqs = [Sequence.create(line) for line in lines]
    logger.info(f"{seqs[:3]=}...")

    res_1 = sum(seq.get_next() for seq in seqs)
    logger.info(f"{res_1=}")

    res_2 = sum(seq.get_prev() for seq in seqs)
    logger.info(f"{res_2=}")

    return res_1, res_2
