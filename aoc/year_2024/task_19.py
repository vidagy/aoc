import logging

from cachetools import LRUCache, cached
from pygtrie import CharTrie

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line, tokenize

logger = logging.getLogger(__name__)


def is_possible(design: str, supply: CharTrie) -> bool:
    @cached(cache=LRUCache(maxsize=2**20))
    def _is_possible(design: str) -> bool:
        if not design:
            return True
        for prefix in supply.prefixes(design):
            if prefix.value and _is_possible(design[len(prefix.key) :]):
                return True
        return False

    return _is_possible(design)


def number_of_possible_combinations(design: str, supply: CharTrie) -> int:

    @cached(cache=LRUCache(maxsize=2**20))
    def _number_of_possible_combinations(design: str) -> int:
        if not design:
            return 1
        res = 0
        for prefix in supply.prefixes(design):
            if prefix.value:
                res += _number_of_possible_combinations(design[len(prefix.key) :])
        return res

    return _number_of_possible_combinations(design)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_supply, designs = split_lines_by_empty_line(reader.file_to_lines(19))
    supply = CharTrie.fromkeys(tokenize(raw_supply)[0], value=True)

    # logger.info(f"{supply[:3]=}...")
    logger.info(f"{designs[:3]=}...")

    res_1 = sum(1 for design in designs if is_possible(design, supply))
    logger.info(f"{res_1=}")

    res_2 = sum(
        number_of_possible_combinations(design, supply)
        for design in designs
        if is_possible(design, supply)
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
