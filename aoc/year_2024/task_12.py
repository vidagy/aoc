import logging
from collections import defaultdict
from typing import Generator, Iterable, Optional

from networkx import Graph, connected_components

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize_by_char

logger = logging.getLogger(__name__)


def neighbors(
    x: int, y: int, raw_map: list[list[str]]
) -> Generator[tuple[int, int, Optional[str]], None, None]:
    n_x = len(raw_map)
    n_y = len(raw_map[0])

    for d_x, d_y in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        new_x = x + d_x
        new_y = y + d_y
        yield new_x, new_y, (
            raw_map[new_x][new_y] if 0 <= new_x < n_x and 0 <= new_y < n_y else None
        )


class Clusters:
    def __init__(self, raw_map: list[list[str]]) -> None:
        g = Graph()

        for x, line in enumerate(raw_map):
            for y, c in enumerate(line):
                g.add_node((x, y), label=c, border=set())
                for nx, ny, nc in neighbors(x, y, raw_map):
                    if c == nc:
                        g.add_edge((x, y), (nx, ny))
                    else:
                        g.nodes[(x, y)]["border"].add((nx, ny))

        self.graph = g


def fence_cost(graph: Graph, cluster: set[tuple[int, int]]) -> int:
    area = len(cluster)
    perimeter = sum(len(graph.nodes[node]["border"]) for node in cluster)

    return area * perimeter


def count_intervals(nums: set[int]) -> int:
    sorted_nums = list(nums)
    sorted_nums.sort()
    if len(sorted_nums) < 1:
        return 0

    res = 1
    pre = sorted_nums[0]
    for num in sorted_nums[1:]:
        if pre + 1 != num:
            res += 1
        pre = num
    return res


def count_in_a_row(
    index: int,
    dir: list[int],
    rows: Iterable[set[tuple[int, int]]],
    cluster: set[tuple[int, int]],
):
    res = 0
    for row in rows:
        nums = set()
        for n in row:
            c = (dir[0] + n[0], dir[1] + n[1])
            if c in cluster:
                nums.add(c[1 - index])
        res += count_intervals(nums)
    return res


def count_borders_x(
    cluster: set[tuple[int, int]], neighbors: set[tuple[int, int]], index: int
) -> int:
    res = 0
    neighbor_rows = defaultdict(set)
    for n in neighbors:
        neighbor_rows[n[index]].add(n)

    dir = [0, 0]
    dir[index] = 1

    res += count_in_a_row(index, dir, neighbor_rows.values(), cluster)

    dir = [-1 * dir[0], -1 * dir[1]]
    res += count_in_a_row(index, dir, neighbor_rows.values(), cluster)
    return res


def discounted_fence_cost(graph: Graph, cluster: set[tuple[int, int]]) -> int:
    neighbors = {n for node in cluster for n in graph.nodes[node]["border"]}
    perimeter = count_borders_x(cluster, neighbors, index=0) + count_borders_x(
        cluster, neighbors, index=1
    )
    return len(cluster) * perimeter


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_map = tokenize_by_char(reader.file_to_lines(12))
    logger.info(f"{[l[:3] for l in raw_map[:3]]=}...")

    clusters = Clusters(raw_map)

    res_1 = sum(
        fence_cost(clusters.graph, set(cluster))
        for cluster in connected_components(clusters.graph)
    )
    logger.info(f"{res_1=}")

    res_2 = sum(
        discounted_fence_cost(clusters.graph, set(cluster))
        for cluster in connected_components(clusters.graph)
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
