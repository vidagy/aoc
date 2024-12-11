import logging

from networkx import DiGraph, subgraph_view, topological_sort

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, split_lines_by_empty_line, tokenize

logger = logging.getLogger(__name__)


def build_order_graph(order_inp: list[list[int]]) -> DiGraph:
    res = DiGraph()
    for i, j in order_inp:
        res.add_edge(i, j)
    return res


def is_update_ordered(line: list[int], order: DiGraph) -> bool:
    if len(line) < 2:
        return True

    line_set = set(line)
    filtered_order = subgraph_view(order, filter_node=lambda node: node in line_set)

    return line == list(topological_sort(filtered_order))


def order_line(line: list[int], order: DiGraph) -> list[int]:
    line_set = set(line)
    filtered_order = subgraph_view(order, filter_node=lambda node: node in line_set)
    return list(topological_sort(filtered_order))


def get_order_and_updates(
    lines: list[str],
) -> tuple[DiGraph, list[list[int]]]:
    ordering_lines, updates_lines = split_lines_by_empty_line(lines)
    logger.info(f"{ordering_lines[:3]=}...")
    logger.info(f"{updates_lines[:3]=}...")

    order = build_order_graph(convert(tokenize(ordering_lines, separator="|"), int))
    updates = convert(tokenize(updates_lines, separator=","), int)

    return order, updates


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    order, updates = get_order_and_updates(reader.file_to_lines(5))

    res_1 = sum(
        line[len(line) // 2] for line in updates if is_update_ordered(line, order)
    )
    logger.info(f"{res_1=}")

    res_2 = sum(
        order_line(line, order)[len(line) // 2]
        for line in updates
        if not is_update_ordered(line, order)
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
