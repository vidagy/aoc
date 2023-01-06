import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import product

from networkx import DiGraph

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def parse_line(line: str) -> tuple[str, int, list[str]]:
    reg = re.compile(
        r"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z ,]+)"
    )
    groups = reg.match(line).groups()  # type: ignore
    return groups[0], int(groups[1]), groups[2].split(", ")  # type: ignore


@dataclass(frozen=True, unsafe_hash=True)
class Valve:
    name: str
    flow: int

    def __repr__(self) -> str:
        return f"{self.name}[{self.flow:02d}]"


def build_graph(valves: list[tuple[str, int, list[str]]]) -> DiGraph:
    graph = DiGraph()

    valves_by_name: dict[str, Valve] = {
        name: Valve(name, flow) for name, flow, _ in valves
    }

    for name, flow, neighbors in valves:
        graph.add_node(valves_by_name[name])
        for neighbor in neighbors:
            graph.add_edge(valves_by_name[name], valves_by_name[neighbor])

    return graph


@dataclass(frozen=True, unsafe_hash=True)
class WalkState:
    valves: tuple[Valve, ...]
    is_open: frozenset[Valve]
    time: int

    def get_pressure_difference(self, previous_state: "WalkState") -> int:
        opened_valves = self.is_open.difference(previous_state.is_open)
        return sum(v.flow for v in opened_valves)

    def out_valves(self, base_graph: DiGraph) -> dict[Valve, set[Valve]]:
        return {v: {n for _, n in base_graph.out_edges(v)} for v in self.valves}

    def closed_valves(self) -> set[Valve]:
        return {v for v in self.valves if v not in self.is_open and v.flow > 0}

    def possible_next_valves(self, base_graph: DiGraph) -> dict[Valve, set[Valve]]:
        valve_to_out_valves = self.out_valves(base_graph)
        closed_valves = self.closed_valves()
        for v in closed_valves:
            valve_to_out_valves[v].add(v)

        return valve_to_out_valves

    def possible_next_states(self, base_graph: DiGraph) -> set[tuple[Valve, ...]]:
        next_states: set[tuple[Valve, ...]] = set()

        valve_to_out_valves = self.possible_next_valves(base_graph)
        valve_to_steps = [valve_to_out_valves[v] for v in self.valves]
        for new_valves in product(*valve_to_steps):
            next_states.add(new_valves)

        return next_states

    def __repr__(self) -> str:
        valves = sorted(list(v for v in self.valves), key=lambda v: v.name)
        name = f"{self.time:02d}+" + "".join(
            f"{v.name}[{v.flow:02d},{'O' if v in self.is_open else 'C'}]"
            for v in valves
        )
        return name


def my_logger(*args, **kwargs) -> None:
    if False:
        logger.info(*args, **kwargs)


def get_best_step(
    next_valve: tuple[Valve, ...],
    these_states: set[WalkState],
    time_graph: DiGraph,
    max_time: int,
) -> tuple[WalkState, WalkState, dict]:
    choices = [
        (
            this_state,
            time_graph.nodes[this_state]["acc_pressure"]
            + time_graph.nodes[this_state]["pressure"],
            time_graph.nodes[this_state]["pressure"],
            time_graph.nodes[this_state]["acc_pressure"]
            + time_graph.nodes[this_state]["pressure"] * (max_time - this_state.time),
        )
        for this_state in these_states
    ]
    this_state, max_acc_pressure, max_pressure, _ = max(
        choices,
        key=lambda x: x[3],
    )

    opened_valves = {
        v_1 for v_1, v_2 in zip(this_state.valves, next_valve) if v_1 == v_2
    }
    next_state = WalkState(
        valves=next_valve,
        is_open=frozenset(opened_valves.union(this_state.is_open)),
        time=this_state.time + 1,
    )

    data = {
        "acc_pressure": max_acc_pressure,
        "pressure": max_pressure + next_state.get_pressure_difference(this_state),
        "path": time_graph.nodes[this_state]["path"] + [this_state],
    }
    my_logger(
        f" -> from {this_state} to {next_state} of %s",
        [f"{s}:{c:03d}" for s, _, _, c in choices],
    )

    return this_state, next_state, data


def get_next_states(
    this_states: set[WalkState], base_graph: DiGraph, time_graph: DiGraph, max_time: int
) -> list[tuple[WalkState, WalkState, dict]]:
    next_valves_to_from_states = defaultdict(set)
    for this_state in this_states:
        next_valves = this_state.possible_next_states(base_graph)
        for next_valve in next_valves:
            next_valves_to_from_states[next_valve].add(this_state)

    return [
        get_best_step(next_valve, these_states, time_graph, max_time)
        for next_valve, these_states in next_valves_to_from_states.items()
    ]


def build_time_graph(base_graph: DiGraph, max_time: int, num_walkers: int) -> DiGraph:
    time_graph = DiGraph()

    # set up starting state
    base_start = [v for v in base_graph.nodes if v.name == "AA"][0]
    start_valves = tuple(base_start for _ in range(num_walkers))
    start_state = WalkState(valves=start_valves, is_open=frozenset(), time=0)
    time_graph.add_node(start_state, acc_pressure=0, pressure=0, path=[])

    previous_states = {start_state}

    for time in range(1, max_time + 1):
        my_logger("")
        my_logger("")
        my_logger("------------------------")
        my_logger("----------%2d----------", time)
        my_logger("------------------------")
        my_logger("")

        # print_graph(time_graph)

        my_logger(f"{previous_states=}")
        these_states: set[WalkState] = set()

        next_states = get_next_states(previous_states, base_graph, time_graph, max_time)
        for from_state, to_state, data in next_states:
            my_logger(f" -> (!!!) Stepping: {from_state} -> {to_state}")
            these_states.add(to_state)
            time_graph.add_node(to_state, **data)
            time_graph.add_edge(from_state, to_state)

        previous_states = these_states
    return time_graph


def print_graph(graph: DiGraph) -> None:
    for node in graph.nodes:
        logger.info(f"{node=} -> %s", [o for _, o in graph.out_edges(node)])


def get_max_pressure_released(graph: DiGraph, max_time: int) -> int:
    max_pressure, end = max(
        [
            (d["acc_pressure"], n)
            for n, d in graph.nodes(data=True)
            if n.time == max_time
        ],
        key=lambda x: x[0],
    )

    full_path = graph.nodes[end]["path"] + [end]
    logger.info("Best Path Is:")
    for node in full_path:
        logger.info(
            f"{node} -> %4d, %3d",
            graph.nodes[node]["acc_pressure"],
            graph.nodes[node]["pressure"],
        )
    return max_pressure


test_input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(16)
    # inp = test_input.split("\n")
    valves = [parse_line(line) for line in inp]
    logger.info(f"{valves[:3]=}...")

    graph = build_graph(valves)
    print_graph(graph)
    time_graph = build_time_graph(graph, max_time=30, num_walkers=1)

    print_graph(time_graph)
    res_1 = get_max_pressure_released(time_graph, max_time=30)
    logger.info(f"{res_1=}")

    # time_graph_2 = build_time_graph(graph, max_time=26, num_walkers=2)
    # res_2 = get_max_pressure_released(time_graph_2, max_time=26)
    # logger.info(f"{res_2=}")

    return res_1, 0
