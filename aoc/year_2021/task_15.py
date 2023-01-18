import logging

from networkx import DiGraph, dijkstra_path

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize_by_char

logger = logging.getLogger(__name__)


def get_neighbors(x: int, y: int, width: int, height: int) -> list[tuple[int, int]]:
    x_n = [(xx, y) for xx in [x + 1, x - 1] if 0 <= xx < width]
    y_n = [(x, yy) for yy in [y + 1, y - 1] if 0 <= yy < height]
    return x_n + y_n


def create_graph(cave: list[list[int]]) -> DiGraph:
    height = len(cave)
    width = len(cave[0])
    graph = DiGraph()

    for j, line in enumerate(cave):
        for i, risk in enumerate(line):
            graph.add_node((i, j), weight=risk)
            for x, y in get_neighbors(i, j, width, height):
                graph.add_edge((x, y), (i, j))

    return graph


def get_min_path(graph: DiGraph, cave: list[list[int]]) -> int:
    start = (0, 0)
    end = len(cave[0]) - 1, len(cave) - 1

    def func(_, v, __) -> int:
        node_v_wt = graph.nodes[v]["weight"]
        return node_v_wt

    path = dijkstra_path(graph, start, end, weight=func)

    weight = sum(cave[y][x] for x, y in path[1:])
    return weight


def extend_cave(times: int, cave: list[list[int]]) -> list[list[int]]:
    res: list[list[int]] = []
    for jj in range(times):
        for j, line in enumerate(cave):
            new_line: list[int] = []
            for ii in range(times):
                for i, risk in enumerate(line):
                    new_line.append((risk + ii + jj - 1) % 9 + 1)
            res.append(new_line)
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    cave = convert(tokenize_by_char(reader.file_to_lines(15)), int)
    # logger.info(f"{cave[:3]=}...")
    graph = create_graph(cave)

    res_1 = get_min_path(graph, cave)
    logger.info(f"{res_1=}")

    large_cave = extend_cave(5, cave)
    # logger.info(f"{large_cave[:3]=}...")
    large_graph = create_graph(large_cave)
    res_2 = get_min_path(large_graph, large_cave)
    logger.info(f"{res_2=}")

    return res_1, res_2
