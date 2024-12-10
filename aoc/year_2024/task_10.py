import logging
from dataclasses import dataclass
from typing import Iterable

from networkx import DiGraph, all_simple_paths

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize_by_char

logger = logging.getLogger(__name__)


NEIGHBORS = {
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
}


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    h: int

    def neighbors(self, lines: list[list[int]]) -> Iterable["Point"]:
        s_x = len(lines)
        s_y = len(lines[0])
        for d_x, d_y in NEIGHBORS:
            n_x = self.x + d_x
            n_y = self.y + d_y

            if 0 <= n_x < s_x and 0 <= n_y < s_y:
                yield Point(n_x, n_y, lines[n_x][n_y])


class TopographicMap:
    def __init__(self, lines: list[list[int]]) -> None:
        self.trail_heads: set[Point] = set()
        self.peaks: set[Point] = set()

        self.g = DiGraph()
        for x, line in enumerate(lines):
            for y, h in enumerate(line):
                p = Point(x, y, h)
                if h == 0:
                    self.trail_heads.add(p)
                if h == 9:
                    self.peaks.add(p)
                for n in p.neighbors(lines):
                    if n.h == h + 1:
                        self.g.add_edge(p, n)

        self.peak_sink = Point(-1, -1, 10)
        for p in self.peaks:
            self.g.add_edge(p, self.peak_sink)

    def get_trails_from(self, th: Point) -> list[list[Point]]:
        assert th in self.trail_heads
        return [p[:-1] for p in all_simple_paths(self.g, th, self.peak_sink)]

    def get_sum_trail_head_scores(self) -> int:
        return sum(
            len(set(p[-1] for p in self.get_trails_from(th))) for th in self.trail_heads
        )

    def get_sum_trail_head_paths(self) -> int:
        return sum(len(self.get_trails_from(th)) for th in self.trail_heads)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = convert(tokenize_by_char(reader.file_to_lines(10)), int)
    logger.info(f"{lines[:3]=}...")

    topo_map = TopographicMap(lines)

    res_1 = topo_map.get_sum_trail_head_scores()
    logger.info(f"{res_1=}")

    res_2 = topo_map.get_sum_trail_head_paths()
    logger.info(f"{res_2=}")

    return res_1, res_2
