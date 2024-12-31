import logging
from bisect import bisect_left
from dataclasses import dataclass

import networkx as nx

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize

logger = logging.getLogger(__name__)

NEIGHBORS = {
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
}


@dataclass
class Maze:
    holes: set[tuple[int]]
    graph: nx.Graph

    @staticmethod
    def create(lines: list[str], n: int = 1024) -> "Maze":
        holes = {
            tuple(line) for i, line in enumerate(convert(tokenize(lines), int)) if i < n
        }

        return Maze(holes, Maze.build_graph(holes))  # type: ignore

    @staticmethod
    def build_graph(holes: list[tuple[int]]) -> nx.Graph:
        g = nx.Graph()

        for y in range(71):
            for x in range(71):
                if (x, y) in holes:
                    continue
                for d_x, d_y in NEIGHBORS:
                    n_x = x + d_x
                    n_y = y + d_y
                    if 0 <= n_x <= 70 and 0 <= n_y <= 70 and (n_x, n_y) not in holes:
                        g.add_edge((x, y), (n_x, n_y))

        return g


def find_connectivity(lines: list[str]) -> str:
    def comp(line: str) -> int:
        i = lines.index(line)
        maze = Maze.create(lines, n=i + 1)
        try:
            return -1 * nx.shortest_path_length(maze.graph, (0, 0), (70, 70))
        except nx.NetworkXNoPath:
            return 1

    i = bisect_left(lines, 0, lo=1024, key=comp)
    return lines[i]


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, str]:
    lines = reader.file_to_lines(18)
    logger.info(f"{lines[:3]=}...")

    maze = Maze.create(lines)

    res_1 = nx.shortest_path_length(maze.graph, (0, 0), (70, 70))
    logger.info(f"{res_1=}")

    res_2 = find_connectivity(lines)
    logger.info(f"{res_2=}")

    return res_1, res_2
