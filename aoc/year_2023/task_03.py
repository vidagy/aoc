import logging
from collections import defaultdict
from dataclasses import dataclass, field

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass(frozen=True, unsafe_hash=True)
class Gear:
    x: int
    y: int


@dataclass
class Num:
    x: int
    y: int
    val: int
    gear_neighbor: list[Gear] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"[{self.x, self.y}]: {self.val}"

    @staticmethod
    def extract_from_line(n: int, line: str) -> list["Num"]:
        nums = []

        active = line[0].isdecimal()
        val = 0
        for j, c in enumerate(line):
            if c.isdecimal():
                active = True
                val = val * 10 + int(c)
            elif active:
                active = False
                nums.append(Num(n, j - len(str(val)), val))
                val = 0
        if active:
            nums.append(Num(n, len(line) - len(str(val)), val))
        return nums

    def add_gears(self, frame: list[tuple[int, int]], lines: list[str]) -> None:
        for x, y in frame:
            if lines[x][y] == "*":
                self.gear_neighbor.append(Gear(x, y))


def is_special_character(c: str) -> bool:
    if len(c) != 1:
        raise Exception(f"Expected a single char but got {c=}")
    return c != "." and not c.isdecimal()


def get_frame(n_x: int, n_y: int, num: Num) -> list[tuple[int, int]]:
    def in_canvas(x: int, y: int) -> bool:
        return x >= 0 and x < n_x and y >= 0 and y < n_y

    res = []
    for i in range(num.x - 1, num.x + 2):
        for j in range(num.y - 1, num.y + len(str(num.val)) + 1):
            if not (i == num.x and num.y <= j < num.y + len(str(num.val))):
                if in_canvas(i, j):
                    res.append((i, j))
    return res


def get_nums_next_to_symbols(
    n_x: int, n_y: int, nums: list[Num], lines: list[str]
) -> list[Num]:
    res = []
    for num in nums:
        frame = get_frame(n_x, n_y, num)
        if any(is_special_character(lines[x][y]) for x, y in frame):
            num.add_gears(frame, lines)
            res.append(num)
    return res


def get_gears_to_nums(nums: list[Num]) -> dict[Gear, list[Num]]:
    res = defaultdict(list)
    for num in nums:
        for gear in num.gear_neighbor:
            res[gear].append(num)

    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(3)
    logger.info(f"{lines[:3]=}...")

    n_x = len(lines)
    n_y = len(lines[0])

    logger.info(f"{n_x=} {n_y=}")

    nums = [
        num for n, line in enumerate(lines) for num in Num.extract_from_line(n, line)
    ]
    logger.info(f"{nums[:33]=}...")
    nums_next_to_symbols = get_nums_next_to_symbols(n_x, n_y, nums, lines)

    res_1 = sum(n.val for n in nums_next_to_symbols)
    logger.info(f"{res_1=}")

    gears_to_nums = get_gears_to_nums(nums_next_to_symbols)
    res_2 = sum(
        nums[0].val * nums[1].val
        for gear, nums in gears_to_nums.items()
        if len(nums) == 2
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
