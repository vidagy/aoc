import logging
from dataclasses import dataclass
from typing import Generator

import networkx as nx

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize_by_char

logger = logging.getLogger(__name__)

NEIGHBORS = {
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
}


HUGE_WEIGHT = 2**20


@dataclass
class Maze:
    raw: list[list[str]]
    graph: nx.Graph
    start: tuple[int, int]
    end: tuple[int, int]
    n_x: int
    n_y: int

    @staticmethod
    def contains(x: int, y: int, n_x: int, n_y: int) -> bool:
        return 0 <= x < n_x and 0 <= y < n_y

    @staticmethod
    def all_neighbors(
        x: int, y: int, n_x: int, n_y: int
    ) -> Generator[tuple[int, int], None, None]:
        for d_x, d_y in NEIGHBORS:
            xx = x + d_x
            yy = y + d_y
            if Maze.contains(xx, yy, n_x, n_y):
                yield xx, yy

    @staticmethod
    def simple_cheats(
        x: int, y: int, n_x: int, n_y: int, raw: list[list[str]]
    ) -> Generator[tuple[int, int], None, None]:
        for xx, yy in Maze.all_neighbors(x, y, n_x, n_y):
            if raw[xx][yy] == "#":
                for xxx, yyy in Maze.all_neighbors(xx, yy, n_x, n_y):
                    if (x != xxx or y != yyy) and raw[xxx][yyy] != "#":
                        yield (xxx, yyy)

    @staticmethod
    def k_cheats(
        x: int, y: int, n_x: int, n_y: int, raw: list[list[str]], k: int
    ) -> Generator[tuple[int, int], None, None]:
        for x_diff in range(-k, k + 1):
            y_range = k - abs(x_diff)
            for y_diff in range(-y_range, y_range + 1):
                xx = x + x_diff
                yy = y + y_diff
                if Maze.contains(xx, yy, n_x, n_y) and raw[xx][yy] != "#":
                    yield (xx, yy)

    @staticmethod
    def create(raw: list[list[str]]) -> "Maze":
        n_x = len(raw)
        n_y = len(raw[0])
        start = (0, 0)
        end = (0, 0)
        g = nx.Graph()

        for x, line in enumerate(raw):
            for y, c in enumerate(line):
                if c == "#":
                    continue
                if c == "S":
                    start = x, y
                if c == "E":
                    end = x, y

                for xx, yy in Maze.all_neighbors(x, y, n_x, n_y):
                    cc = raw[xx][yy]
                    if cc != "#":
                        g.add_edge((x, y), (xx, yy))

        return Maze(raw, g, start, end, n_x, n_y)

    def gen_all_paths(self) -> None:
        self.all_paths = nx.single_source_shortest_path(self.graph, self.end)

    def num_simple_cheats_that_save_at_least_n(self, n: int = 100):
        shortest_path = self.all_paths[self.start]
        shortest_path_length = len(shortest_path) - 1

        res = 0

        for length_so_far, node in enumerate(shortest_path[::-1]):
            x, y = node
            for xxx, yyy in Maze.simple_cheats(x, y, self.n_x, self.n_y, self.raw):
                if (xxx, yyy) not in self.all_paths:
                    continue
                new_len = length_so_far + 1 + len(self.all_paths[(xxx, yyy)])
                if new_len <= shortest_path_length - n:
                    res += 1
        return res

    def num_longer_cheats_that_save_at_least_n(self, n: int = 100, k: int = 20):
        shortest_path = self.all_paths[self.start]
        shortest_path_length = len(shortest_path) - 1

        res = 0

        for length_so_far, node in enumerate(shortest_path[::-1]):
            x, y = node
            for xxx, yyy in Maze.k_cheats(x, y, self.n_x, self.n_y, self.raw, k):
                if (xxx, yyy) not in self.all_paths:
                    continue
                new_len = (
                    length_so_far
                    + abs(x - xxx)
                    + abs(y - yyy)
                    - 1
                    + len(self.all_paths[(xxx, yyy)])
                )
                if new_len <= shortest_path_length - n:
                    res += 1
        return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_maze = tokenize_by_char(reader.file_to_lines(20))
    logger.info(f"{raw_maze[:3]=}...")

    maze = Maze.create(raw_maze)
    maze.gen_all_paths()

    res_1 = maze.num_simple_cheats_that_save_at_least_n()
    logger.info(f"{res_1=}")

    res_2 = maze.num_longer_cheats_that_save_at_least_n(n=100, k=20)
    logger.info(f"{res_2=}")

    return res_1, res_2
