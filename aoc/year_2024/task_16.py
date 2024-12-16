import logging
from dataclasses import dataclass

import networkx as nx

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize_by_char

logger = logging.getLogger(__name__)


@dataclass(frozen=True, unsafe_hash=True)
class State:
    x: int
    y: int
    dir: str


MOVEMENTS = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}


class Labyrinth:
    def __init__(self, lines: list[list[str]]) -> None:
        self.n_x = len(lines)
        self.n_y = len(lines[0])
        g = nx.DiGraph()
        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                if c == "#":
                    continue

                self.add_edges(g, x, y, lines)

                if c == "S":
                    self.start = State(x, y, ">")
                if c == "E":
                    self.end = State(x, y, "#")
                    for d in [">", "<", "^", "v"]:
                        g.add_edge(State(x, y, d), self.end, weight=0)
        self.g = g

    def add_edges(self, g: nx.DiGraph, x: int, y: int, lines: list[list[str]]) -> None:
        for d in [">", "<", "^", "v"]:
            s = State(x, y, d)
            dest_x = MOVEMENTS[d][0] + x
            dest_y = MOVEMENTS[d][1] + y
            if (
                0 <= dest_x < self.n_x
                and 0 <= dest_y < self.n_y
                and lines[dest_x][dest_y] != "#"
            ):
                g.add_edge(s, State(dest_x, dest_y, d), weight=1)
            if d in {"<", ">"}:
                for dd in ["^", "v"]:
                    g.add_edge(s, State(x, y, dd), weight=1000)
            if d in {"^", "v"}:
                for dd in ["<", ">"]:
                    g.add_edge(s, State(x, y, dd), weight=1000)

    def get_shortest_path_length(self) -> int:
        return nx.shortest_path_length(self.g, self.start, self.end, weight="weight")

    def get_len_all_shortest_path_nodes(self) -> int:
        res: set[tuple[int, int]] = set()
        for path in nx.all_shortest_paths(
            self.g, self.start, self.end, weight="weight"
        ):
            for state in path:
                res.add((state.x, state.y))
        return len(res)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = tokenize_by_char(reader.file_to_lines(16))
    logger.info(f"{lines[:3]=}...")
    labyrinth = Labyrinth(lines)

    res_1 = labyrinth.get_shortest_path_length()
    logger.info(f"{res_1=}")

    res_2 = labyrinth.get_len_all_shortest_path_nodes()
    logger.info(f"{res_2=}")

    return res_1, res_2
