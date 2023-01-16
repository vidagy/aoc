import logging
from collections import Counter

from cachetools import cached
from cachetools.keys import hashkey

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line, tokenize

logger = logging.getLogger(__name__)


def evolve(input_line: str, rules: dict[str, str]) -> str:
    out = input_line[0]
    pre_c = input_line[0]
    for i in range(1, len(input_line)):
        c = input_line[i]
        x = pre_c + c
        if x in rules:
            out += rules[x]
        out += c
        pre_c = c

    return out


@cached(cache={}, key=lambda depth, left, right, rules: hashkey(depth, left, right))  # type: ignore
def evolve_dfs(depth: int, left: str, right: str, rules: dict[str, str]) -> Counter:
    counter: Counter = Counter()
    if depth == 0:
        return counter

    what = left + right
    if what not in rules:
        return counter

    mid = rules[what]
    counter[mid] += 1
    counter += evolve_dfs(depth - 1, left, mid, rules)
    counter += evolve_dfs(depth - 1, mid, right, rules)

    return counter


def get_res(depth: int, input_line: str, rules: dict[str, str]) -> int:
    counter: Counter = Counter()
    left = input_line[0]
    counter[left] += 1
    for right in input_line[1:]:
        counter += evolve_dfs(depth, left, right, rules)
        left = right
        counter[left] += 1

    counts = sorted(list(counter.values()))
    return counts[-1] - counts[0]


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(14)
    lines = split_lines_by_empty_line(inp)
    input_line = lines[0][0]
    rules = {k: v for k, v in tokenize(lines[1], " -> ")}

    res_1 = get_res(10, input_line, rules)
    logger.info(f"{res_1=}")

    res_2 = get_res(40, input_line, rules)
    logger.info(f"{res_2=}")

    return res_1, res_2
