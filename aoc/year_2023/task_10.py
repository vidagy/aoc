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

    def find_steps(self, lines: list[str]) -> list[Pos]:
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
                        return path
                    except exception.NetworkXNoPath:
                        pass
        raise Exception("blaa")


def add_node_to_domains(node: Pos, domains: set[set[Pos]]) -> None:
    new_domain = {node}
    neighbors = {
        Pos(0, 1) + node,
        Pos(0, -1) + node,
        Pos(1, 0) + node,
        Pos(-1, 0) + node,
    }
    for domain in domains:
        if node in domain:
            return
        is_touch = any(n in domain for n in neighbors)
        if is_touch:
            new_domain = new_domain.union(domain)
            domains.remove(domain)

    domains.add(new_domain)


def grow_domain(
    domain: set[Pos], domains: set[set[Pos]], path: list[Pos], lines: list[str]
) -> None:
    N_x = len(lines)
    N_y = len(lines[0])
    for node in domain:
        neighbors = {
            Pos(0, 1) + node,
            Pos(0, -1) + node,
            Pos(1, 0) + node,
            Pos(-1, 0) + node,
        }
        for n in neighbors:
            if n not in domain and n not in path and 0 <= n.x < N_x and 0 <= n.y < N_y:
                add_node_to_domains(n, domains)


def grow_domains(domains: set[set[Pos]], path: list[Pos], lines: list[str]) -> None:
    prev_domains: set[set[Pos]] = set()
    while True:
        for domain in domains:
            grow_domain(domain, domains, path, lines)

        if prev_domains == domains:
            return

        prev_domains = deepcopy(domains)


def count_containment(path: list[Pos], lines: list[str]) -> int:
    path_set = set(path)
    domains: set[set[Pos]] = set()
    for node in path_set:
        neighbors = PIPE_TO_NEIGHBORS[lines[node.x][node.y]]
        for neighbor in neighbors:
            pos_n = neighbor + node
            if pos_n not in path_set and all(pos_n not in domain for domain in domains):
                add_node_to_domains(pos_n, domains)

    grow_domains(domains, path, lines)

    for domain in domains:
        logger.info(f"{len(domain)=} {domain=}")

    return 1


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(10)
    logger.info(f"{lines[:3]=}...")

    pipes = Pipes.create(lines)
    path = pipes.find_steps(lines)
    path.insert(0, pipes.start)
    path.append(pipes.start)
    res_1 = len(path) // 2
    logger.info(f"{res_1=}")

    res_2 = count_containment(path, lines)
    logger.info(f"{res_2=}")

    return res_1, res_2
