import logging
from copy import deepcopy

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class Matcher:
    def __init__(self, i: int) -> None:
        self.i = i

    def __eq__(self, __o: object) -> bool:
        return __o[1] == self.i  # type: ignore


def do_the_thing(numbers: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # logger.info(f"      {[n for n in numbers]}")
    size = len(numbers)
    for i in range(len(numbers)):
        try:
            index = numbers.index(Matcher(i))  # type: ignore
            n, ni = numbers.pop(index)
            new_pos = (index + n) % (size - 1)
            numbers.insert(new_pos, (n, ni))
            # logger.info(f"{n=:3d} {[n for n, _ in inp]}")

        except ValueError:
            break
    return numbers


def get_res(inp: list[tuple[int, int]]) -> int:
    nums = [n for n, _ in inp]
    i = nums.index(0)
    x = nums[(i + 1000) % len(nums)]
    y = nums[(i + 2000) % len(nums)]
    z = nums[(i + 3000) % len(nums)]
    logger.info(f"{i=} {nums[i]=} {x=} {y=} {z=}")
    return x + y + z


test_inp = """1
2
-3
3
-2
0
4"""


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(20)
    # inp = test_inp.split("\n")
    numbers = [(int(n), i) for i, n in enumerate(inp)]
    logger.info(f"{numbers[:3]=}")

    numbers_transformed = do_the_thing(deepcopy(numbers))
    res_1 = get_res(numbers_transformed)
    logger.info(f"{res_1=}")

    numbers_2 = [(n * 811589153, i) for n, i in numbers]
    for _ in range(10):
        numbers_2 = do_the_thing(numbers_2)
        # logger.info(f"{numbers_2=}")
    res_2 = get_res(numbers_2)
    logger.info(f"{res_2=}")

    return res_1, res_2
