import logging
from dataclasses import dataclass

import networkx as nx

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


START_POS = "S"
GARDEN_PLOT = "."
ROCK = "#"


@dataclass(unsafe_hash=True, eq=True)
class Plot:
    x: int
    y: int


@dataclass
class Garden:
    plots: list[str]

    def __post_init__(self) -> None:
        self.n_x: int = len(self.plots)
        self.n_y: int = len(self.plots[0])

        for x, line in enumerate(self.plots):
            for y, c in enumerate(line):
                if c == START_POS:
                    self.start_pos: Plot = Plot(x, y)
                    return


def build_garden_graph(garden: Garden) -> nx.Graph:
    graph = nx.Graph()
    for x, line in enumerate(garden.plots[1:], start=1):
        for y, c in enumerate(line[1:], start=1):
            if c == ROCK:
                continue

            # left
            left_x = x - 1
            left_y = y
            if garden.plots[left_x][left_y] != ROCK:
                graph.add_edge(Plot(x, y), Plot(left_x, left_y))

            # down
            down_x = x
            down_y = y - 1
            if garden.plots[down_x][down_y] != ROCK:
                graph.add_edge(Plot(x, y), Plot(down_x, down_y))

    return graph


def count_reachable_in(limit: int, start: Plot, graph: nx.Graph) -> int:
    nx.set_node_attributes(graph, None, "steps")
    nx.set_node_attributes(graph, False, "ever_even")
    nx.set_node_attributes(graph, False, "ever_odd")

    backlog: list[Plot] = [start]
    graph.nodes[start]["steps"] = 0
    graph.nodes[start]["ever_even"] = True
    graph.nodes[start]["ever_odd"] = False

    while backlog:
        current = backlog.pop(0)
        current_steps = graph.nodes[current]["steps"]
        if current_steps == limit:
            continue
        for _, next in graph.edges(current):
            next_steps = graph.nodes[next]["steps"]
            next_ever_even = graph.nodes[next]["ever_even"]
            next_ever_odd = graph.nodes[next]["ever_odd"]
            next_potential_odd = bool((current_steps + 1) % 2)
            # will visit neighbor when
            if (
                # neighbor has never been visited before
                next_steps is None
                or
                # next has never been odd but now it can
                (not next_ever_odd and next_potential_odd)
                or
                # next has never been even but now it can
                (not next_ever_even and not next_potential_odd)
            ):
                graph.nodes[next]["steps"] = current_steps + 1
                graph.nodes[next]["ever_odd"] = next_ever_odd or next_potential_odd
                graph.nodes[next]["ever_even"] = (
                    next_ever_even or not next_potential_odd
                )
                backlog.append(next)

    return sum(1 for _, ever_even in graph.nodes(data="ever_even") if ever_even)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(21)
    garden = Garden(lines)
    garden_graph = build_garden_graph(garden)

    res_1 = count_reachable_in(64, garden.start_pos, garden_graph)
    logger.info(f"{res_1=}")

    res_2 = 0
    logger.info(f"{res_2=}")

    return res_1, res_2
