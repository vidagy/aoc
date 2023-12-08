import logging
import math
from dataclasses import dataclass
from itertools import cycle
from typing import Callable

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


@dataclass
class NodeMap:
    mapping: dict[str, tuple[str, str]]

    @staticmethod
    def read(raw_node_map: list[str]) -> "NodeMap":
        mapping: dict[str, tuple[str, str]] = {}
        for line in raw_node_map:
            source, dest = line.split("=")
            mapping[source.strip()] = tuple(
                d.strip() for d in dest.strip("() ").split(",")
            )  # type: ignore
        return NodeMap(mapping)

    def find_path(
        self, directions: str, start: str, end_predicate: Callable[[str], bool]
    ) -> list[str]:
        path = [start]
        last = path[-1]
        for direction in cycle(directions):
            if end_predicate(last):
                break
            last = self.mapping[last][0 if direction == "L" else 1]
            path.append(last)

        return path

    def find_all_start_nodes(self) -> list[str]:
        all_nodes = set(self.mapping.keys())
        for left, right in self.mapping.values():
            all_nodes.add(left)
            all_nodes.add(right)
        starts = list(set(node for node in all_nodes if node.endswith("A")))
        return starts

    def find_ghost_path_length(self, directions: str) -> int:
        starts = self.find_all_start_nodes()
        cycle_lengths = set()
        for s in starts:
            length = (
                len(
                    self.find_path(
                        directions, start=s, end_predicate=lambda x: x.endswith("Z")
                    )
                )
                - 1
            )
            cycle_lengths.add(length)

        return math.lcm(*cycle_lengths)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(8)

    raw_directions, raw_node_map = split_lines_by_empty_line(lines)
    directions = raw_directions[0]
    node_map = NodeMap.read(raw_node_map)

    logger.info(f"{directions[:13]=}")
    # logger.info(f"{node_map.mapping=}")

    res_1 = (
        len(
            node_map.find_path(
                directions, start="AAA", end_predicate=lambda x: x == "ZZZ"
            )
        )
        - 1
    )
    logger.info(f"{res_1=}")

    res_2 = node_map.find_ghost_path_length(directions)
    logger.info(f"{res_2=}")

    return res_1, res_2
