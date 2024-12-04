import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from networkx import Graph, exception, shortest_path

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass(frozen=True, unsafe_hash=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def __mul__(self, num: int) -> "Pos":
        return Pos(num * self.x, num * self.y)


PIPE_TO_CONNECTIONS = {
    "|": [(Pos(-1, 0), Pos(1, 0))],
    "-": [(Pos(0, -1), Pos(0, 1))],
    "L": [(Pos(-1, 0), Pos(0, 1))],
    "J": [(Pos(-1, 0), Pos(0, -1))],
    "7": [(Pos(1, 0), Pos(0, -1))],
    "F": [(Pos(1, 0), Pos(0, 1))],
}

PIPE_TO_NEIGHBORS = {
    "|": [Pos(0, -1), Pos(0, 1)],
    "-": [Pos(-1, 0), Pos(1, 0)],
    "L": [Pos(1, 0), Pos(0, -1)],
    "J": [Pos(1, 0), Pos(0, 1)],
    "7": [Pos(-1, 0), Pos(0, 1)],
    "F": [Pos(-1, 0), Pos(0, -1)],
}


def is_compatible(
    start: Pos,
    end: Pos,
    lines: list[str],
    start_override: Optional[str] = None,
    end_override: Optional[str] = None,
) -> bool:
    N_x = len(lines)
    N_y = len(lines[0])
    if (
        not 0 <= start.x < N_x
        or not 0 <= end.x < N_x
        or not 0 <= start.y < N_y
        or not 0 <= end.y < N_y
    ):
        return False

    s = start_override if start_override else lines[start.x][start.y]
    e = end_override if end_override else lines[end.x][end.y]

    if s not in PIPE_TO_CONNECTIONS or e not in PIPE_TO_CONNECTIONS:
        return False
    s_c = PIPE_TO_CONNECTIONS[s][0]
    e_c = PIPE_TO_CONNECTIONS[e][0]

    return (start + s_c[0] == end or start + s_c[1] == end) and (
        end + e_c[0] == start or end + e_c[1] == start
    )


@dataclass
class Pipes:
    graph: Graph
    start: Pos

    @staticmethod
    def create(lines: list[str]) -> "Pipes":
        graph = Graph()
        start: Optional[Pos] = None

        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                current = Pos(x, y)
                if c == "S":
                    start = current
                elif c == ".":
                    continue
                else:
                    connections = PIPE_TO_CONNECTIONS[c]
                    for f, t in connections:
                        s = current + f
                        if is_compatible(s, current, lines):
                            graph.add_edge(s, current)
                        e = current + t
                        if is_compatible(current, e, lines):
                            graph.add_edge(current, e)
        if not start:
            raise Exception("could not find start")

        return Pipes(graph, start)

    def find_steps(self, lines: list[str]) -> tuple[str, list[Pos]]:
        for s_pipe, neighbors in PIPE_TO_CONNECTIONS.items():
            for step_1, step_2 in neighbors:
                start = self.start + step_1
                end = self.start + step_2

                if (
                    start in self.graph.nodes
                    and end in self.graph.nodes
                    and is_compatible(start, self.start, lines, end_override=s_pipe)
                    and is_compatible(self.start, end, lines, start_override=s_pipe)
                ):
                    try:
                        path = shortest_path(self.graph, start, end)
                        logger.info(
                            f"{start=} {lines[start.x][start.y]=} {end=} {lines[end.x][end.y]=} {s_pipe=} {len(path)=}"
                        )
                        return s_pipe, path
                    except exception.NetworkXNoPath:
                        pass
        raise Exception("blaa")


class LineWalker:
    def __init__(self, path: set[Pos], size_y: int, lines: list[str]) -> None:
        self.path = path
        self.size_y = size_y
        self.lines = lines

        self.num_inside: int = 0
        self.is_inside: bool = False
        self.last_direction: str = ""

    def walk(self, x: int) -> int:
        previous_is_on_path = False
        for y in range(self.size_y):
            current_pos = Pos(x, y)
            is_on_path = current_pos in self.path

            did_step_down = not is_on_path and previous_is_on_path
            did_step_onto = is_on_path and not previous_is_on_path

            if is_on_path and previous_is_on_path:
                did_switch = self.lines[x][y] in {"|", "F", "L"}
                if did_switch:
                    did_step_down = True
                    did_step_onto = True

            if did_step_down:
                previous_dir = self.lines[x][y - 1]
                if (
                    previous_dir == "|"
                    or (self.last_direction == "F" and previous_dir == "J")
                    or (self.last_direction == "L" and previous_dir == "7")
                ):
                    # we crossed a domain
                    self.is_inside = not self.is_inside
                self.last_direction = ""

            if did_step_onto:
                self.last_direction = self.lines[x][y]

            if not is_on_path:
                if self.is_inside:
                    self.num_inside += 1

            previous_is_on_path = is_on_path
        return self.num_inside


def count_containment(path: list[Pos], lines: list[str]) -> int:
    path_set = set(path)
    inside = 0

    for x in range(len(lines)):
        inside += LineWalker(path_set, len(lines[0]), lines).walk(x)

    return inside


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(10)
    logger.info(f"{lines[:3]=}...")

    pipes = Pipes.create(lines)
    s_pipe, path = pipes.find_steps(lines)
    path.insert(0, pipes.start)
    path.append(pipes.start)
    res_1 = len(path) // 2
    logger.info(f"{res_1=}")

    lines[pipes.start.x] = (
        lines[pipes.start.x][: pipes.start.y]
        + s_pipe
        + lines[pipes.start.x][pipes.start.y + 1 :]
    )
    res_2 = count_containment(path, lines)
    logger.info(f"{res_2=}")

    return res_1, res_2
