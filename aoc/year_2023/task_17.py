import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import networkx as nx

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


StepT = tuple[int, int]

STEP: dict[Direction, StepT] = {
    Direction.Up: (-1, 0),
    Direction.Right: (0, 1),
    Direction.Left: (0, -1),
    Direction.Down: (1, 0),
}


@dataclass
class UltraCrucibleMap:
    graph: nx.DiGraph

    @dataclass
    class Node:
        x: int
        y: int
        from_dir: Optional[Direction]

        def __repr__(self) -> str:
            return f"({self.x},{self.y}){self.from_dir.name[0] if self.from_dir is not None else ''}"

        def __hash__(self) -> int:
            return hash((self.x, self.y, self.from_dir))

    def __init__(self, lines: list[str], min_step: int = 4, max_step: int = 10) -> None:
        graph = nx.DiGraph()
        self.n_x = len(lines)
        self.n_y = len(lines[0])

        for x, line in enumerate(lines):
            for y, weight in enumerate(line):
                if x == 0 and y == 0:
                    UltraCrucibleMap.connect_start(graph)
                if x == self.n_x - 1 and y == self.n_y - 1:
                    UltraCrucibleMap.connect_end(graph, x, y, int(weight))

                for dir in STEP.keys():
                    self.connect_nodes(graph, x, y, dir, min_step, max_step, lines)

        self.graph = graph

    @staticmethod
    def connect_start(graph: nx.DiGraph):
        for dir in STEP:
            graph.add_edge(
                UltraCrucibleMap.Node(0, 0, None),
                UltraCrucibleMap.Node(0, 0, dir),
                weight=0,
            )

    @staticmethod
    def connect_end(graph: nx.DiGraph, x: int, y: int, weight: int):
        for dir in STEP:
            graph.add_edge(
                UltraCrucibleMap.Node(x, y, dir),
                UltraCrucibleMap.Node(x, y, None),
                weight=weight,
            )

    def shortest_weights(self) -> int:
        path = nx.shortest_path(
            self.graph,
            UltraCrucibleMap.Node(0, 0, None),
            UltraCrucibleMap.Node(self.n_x - 1, self.n_y - 1, None),
            weight="weight",
        )

        return nx.path_weight(self.graph, path, weight="weight")

    def connect_nodes(
        self,
        graph: nx.DiGraph,
        x: int,
        y: int,
        prev_dir: Direction,
        min_step: int,
        max_step: int,
        lines: list[str],
    ) -> None:
        from_node = UltraCrucibleMap.Node(x, y, prev_dir)

        for dir, (step_x, step_y) in STEP.items():
            if prev_dir == dir or abs(prev_dir.value - dir.value) == 2:
                continue
            cum_weight = 0
            for i in range(0, min_step):
                other_x = x + i * step_x
                other_y = y + i * step_y
                if 0 <= other_x < self.n_x and 0 <= other_y < self.n_y:
                    cum_weight += (
                        0
                        if (other_x == 0 and other_y == 0)
                        else int(lines[other_x][other_y])
                    )
            for i in range(min_step, max_step + 1):
                other_x = x + i * step_x
                other_y = y + i * step_y
                if not (0 <= other_x < self.n_x and 0 <= other_y < self.n_y):
                    break
                to_node = UltraCrucibleMap.Node(other_x, other_y, dir)
                graph.add_edge(from_node, to_node, weight=cum_weight)

                cum_weight += int(lines[other_x][other_y])


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(17)
    logger.info(f"{lines[:3]=}...")

    res_1 = UltraCrucibleMap(lines, 1, 3).shortest_weights()
    logger.info(f"{res_1=}")

    res_2 = UltraCrucibleMap(lines, 4, 10).shortest_weights()
    logger.info(f"{res_2=}")

    return res_1, res_2
