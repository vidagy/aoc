import logging
from dataclasses import dataclass

from networkx import DiGraph, shortest_path_length, single_target_shortest_path_length

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, print_matrix, tokenize_by_char

logger = logging.getLogger(__name__)


def get_graph(height_map: list[list[int]]) -> DiGraph:
    size_y = len(height_map)
    size_x = len(height_map[0])

    graph = DiGraph()

    for j in range(size_y):
        for i in range(size_x):
            this_height = height_map[j][i]
            this_place = Point(i, j)
            if i == 2 and j == 2:
                pass
            # left
            if i > 0 and height_map[j][i - 1] <= this_height + 1:
                graph.add_edge(this_place, Point(i - 1, j))
            # right
            if i < size_x - 1 and height_map[j][i + 1] <= this_height + 1:
                graph.add_edge(this_place, Point(i + 1, j))
            # up
            if j > 0 and height_map[j - 1][i] <= this_height + 1:
                graph.add_edge(this_place, Point(i, j - 1))
            # down
            if j < size_y - 1 and height_map[j + 1][i] <= this_height + 1:
                graph.add_edge(this_place, Point(i, j + 1))

    return graph


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"


def get_map(lines: list[list[str]]) -> tuple[Point, list[list[int]], Point]:
    size_y = len(lines)
    size_x = len(lines[0])

    height_map: list[list[int]] = []

    for j in range(size_y):
        height_map.append([])
        for i in range(size_x):
            h = lines[j][i]
            if h == "S":
                start = Point(i, j)
                h = "a"
            elif h == "E":
                end = Point(i, j)
                h = "z"

            height_map[j].append(ord(h) - ord("a"))

    return start, height_map, end


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(12)
    lines = tokenize_by_char(inp)
    start, height_map, end = get_map(lines)

    logger.info(f"{start=}")
    logger.info(f"{end=}")

    print_matrix(height_map, limit=5, formatter="%02d ")

    graph = get_graph(height_map)

    res_1 = shortest_path_length(graph, start, end)
    logger.info(f"{res_1=}")

    path_lengths = dict(single_target_shortest_path_length(graph, end))
    fom_zero_path_lengths = {
        p: s for p, s in path_lengths.items() if height_map[p.y][p.x] == 0
    }
    res_2 = min(fom_zero_path_lengths.values())
    logger.info(f"{res_2=}")

    return res_1, res_2
