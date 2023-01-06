import logging
import re
from dataclasses import dataclass

from networkx import DiGraph

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

CostsT = tuple[int, int, int]
CountT = tuple[int, int, int, int]


@dataclass
class Cost:
    cost: tuple[int, int, int] = (0, 0, 0)

    def __add__(self, other: "Cost") -> "Cost":
        return Cost(
            (
                self.cost[0] + other.cost[0],
                self.cost[1] + other.cost[1],
                self.cost[2] + other.cost[2],
            )
        )

    def __mul__(self, other: int) -> "Cost":
        return Cost(
            (
                self.cost[0] * other,
                self.cost[1] * other,
                self.cost[2] * other,
            )
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Cost) and (
            self.cost[0] == other.cost[0]
            and self.cost[1] == other.cost[1]
            and self.cost[2] == other.cost[2]
        )

    def __le__(self, other: "Cost") -> bool:
        return (
            self.cost[0] <= other.cost[0]
            and self.cost[1] <= other.cost[1]
            and self.cost[2] <= other.cost[2]
        )

    def __ge__(self, other: "Cost") -> bool:
        return (
            self.cost[0] >= other.cost[0]
            or self.cost[1] >= other.cost[1]
            or self.cost[2] >= other.cost[2]
        )

    def __lt__(self, other: "Cost") -> bool:
        return (
            self.cost[0] < other.cost[0]
            and self.cost[1] < other.cost[1]
            and self.cost[2] < other.cost[2]
        )

    def __gt__(self, other: "Cost") -> bool:
        return (
            self.cost[0] > other.cost[0]
            or self.cost[1] > other.cost[1]
            or self.cost[2] > other.cost[2]
        )


@dataclass(frozen=True, unsafe_hash=True)
class State:
    time: int
    counts: CountT = (0, 0, 0, 0)
    robot_counts: CountT = (1, 0, 0, 0)

    def wallet(self) -> Cost:
        return Cost((self.counts[ORE], self.counts[CLAY], self.counts[OBSIDIAN]))


@dataclass(frozen=True, unsafe_hash=True)
class Blueprint:
    number: int
    costs: tuple[CostsT, CostsT, CostsT, CostsT]

    @staticmethod
    def parse(line: str) -> "Blueprint":
        reg = re.compile(
            r"Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian."
        )
        groups = reg.match(line).groups()  # type: ignore
        return Blueprint(
            number=int(groups[0]),
            costs=(
                (int(groups[1]), 0, 0),
                (int(groups[2]), 0, 0),
                (int(groups[3]), int(groups[4]), 0),
                (int(groups[5]), 0, int(groups[6])),
            ),
        )


class Evolver:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint
        self.bests: dict[CountT, dict[State, State]] = {}
        self.max_geode_robot_count: int = 0

    def evolve(self, this_state: State) -> None:
        wallet = this_state.wallet()

        for machine_to_construct in [None, ORE, CLAY, OBSIDIAN, GEODE]:
            cost = Cost()
            if machine_to_construct is not None:
                cost = Cost(self.blueprint.costs[machine_to_construct])
                if cost > wallet:
                    continue
            if (
                this_state.robot_counts[GEODE]
                + (1 if machine_to_construct == GEODE else 0)
                < self.max_geode_robot_count
            ):
                continue
            new_state = State(
                this_state.time + 1,
                counts=(
                    this_state.counts[ORE]
                    + this_state.robot_counts[ORE]
                    - cost.cost[ORE],
                    this_state.counts[CLAY]
                    + this_state.robot_counts[CLAY]
                    - cost.cost[CLAY],
                    this_state.counts[OBSIDIAN]
                    + this_state.robot_counts[OBSIDIAN]
                    - cost.cost[OBSIDIAN],
                    this_state.counts[GEODE] + this_state.robot_counts[GEODE],
                ),
                robot_counts=(
                    this_state.robot_counts[ORE]
                    + (1 if machine_to_construct == ORE else 0),
                    this_state.robot_counts[CLAY]
                    + (1 if machine_to_construct == CLAY else 0),
                    this_state.robot_counts[OBSIDIAN]
                    + (1 if machine_to_construct == OBSIDIAN else 0),
                    this_state.robot_counts[GEODE]
                    + (1 if machine_to_construct == GEODE else 0),
                ),
            )
            self.add(this_state, new_state)

    @staticmethod
    def is_state_better_than(this_state: State, other_state: State) -> bool:
        return (
            other_state.counts[ORE] <= this_state.counts[ORE]
            and other_state.counts[CLAY] <= this_state.counts[CLAY]
            and other_state.counts[OBSIDIAN] <= this_state.counts[OBSIDIAN]
            and other_state.counts[GEODE] <= this_state.counts[GEODE]
        ) and not (
            other_state.counts[ORE] == this_state.counts[ORE]
            and other_state.counts[CLAY] == this_state.counts[CLAY]
            and other_state.counts[OBSIDIAN] == this_state.counts[OBSIDIAN]
            and other_state.counts[GEODE] == this_state.counts[GEODE]
        )

    def add(self, old_state: State, new_state: State) -> None:
        self.max_geode_robot_count = max(
            new_state.robot_counts[GEODE], self.max_geode_robot_count
        )
        if new_state.robot_counts not in self.bests:
            self.bests[new_state.robot_counts] = {new_state: old_state}
            return

        best_counts = self.bests[new_state.robot_counts]
        if any(self.is_state_better_than(s, new_state) for s in best_counts):
            return

        anything_to_drop = [
            k for k in best_counts if self.is_state_better_than(new_state, k)
        ]

        self.bests[new_state.robot_counts][new_state] = old_state
        for r in anything_to_drop:
            self.bests[new_state.robot_counts].pop(r)
        return

    @property
    def states(self) -> dict[State, State]:
        return {
            old_state: new_state
            for k, v in self.bests.items()
            for old_state, new_state in v.items()
            if k[GEODE] == self.max_geode_robot_count
        }


def build_time_graph(blueprint: Blueprint, max_time: int) -> DiGraph:
    start_state = State(time=0)
    previous_states = {start_state}
    time_graph = DiGraph()

    for time in range(1, max_time + 1):
        # logger.info(f"{time=} {len(previous_states)=}")
        evolver = Evolver(blueprint)
        for state in previous_states:
            evolver.evolve(state)

        these_states = set()
        for new_state, old_state in evolver.states.items():
            # logger.info(f"(!!!) Adding {old_state=} {new_state=}")
            time_graph.add_edge(old_state, new_state)
            these_states.add(new_state)
        previous_states = these_states

    return time_graph


def print_path(time_graph: DiGraph, node: State, blueprint: Blueprint) -> None:
    current_node = node
    path = [current_node]
    while True:
        in_edges = time_graph.in_edges(current_node)
        if not in_edges:
            break
        current_node, _ = next(iter(in_edges))
        path.append(current_node)
    logger.info("PATH:")
    for p in path[::-1]:
        logger.info(p)

    for i in range(0, len(path) - 1):
        this = path[i]
        pre = path[i + 1]
        bought_robots = (
            this.robot_counts[ORE] - pre.robot_counts[ORE],
            this.robot_counts[CLAY] - pre.robot_counts[CLAY],
            this.robot_counts[OBSIDIAN] - pre.robot_counts[OBSIDIAN],
            this.robot_counts[GEODE] - pre.robot_counts[GEODE],
        )
        robot_costs = (
            Cost(blueprint.costs[ORE]) * bought_robots[ORE]
            + Cost(blueprint.costs[CLAY]) * bought_robots[CLAY]
            + Cost(blueprint.costs[OBSIDIAN]) * bought_robots[OBSIDIAN]
            + Cost(blueprint.costs[GEODE]) * bought_robots[GEODE]
        )
        production = (
            pre.robot_counts[ORE],
            pre.robot_counts[CLAY],
            pre.robot_counts[OBSIDIAN],
            pre.robot_counts[GEODE],
        )
        assert (
            this.counts[ORE]
            == pre.counts[ORE] + production[ORE] - robot_costs.cost[ORE]
        )
        assert (
            this.counts[CLAY]
            == pre.counts[CLAY] + production[CLAY] - robot_costs.cost[CLAY]
        )
        assert (
            this.counts[OBSIDIAN]
            == pre.counts[OBSIDIAN] + production[OBSIDIAN] - robot_costs.cost[OBSIDIAN]
        )
        assert this.counts[GEODE] == pre.counts[GEODE] + production[GEODE]


def max_geode(blueprint: Blueprint, max_time: int) -> int:
    time_graph = build_time_graph(blueprint, max_time)
    m = max(
        (state for state in time_graph.nodes if state.time == max_time),
        key=lambda s: s.counts[GEODE],
    )
    logger.info(f"{m=}")
    # print_path(time_graph, m, blueprint)

    return m.counts[GEODE]


example = Blueprint(
    number=1,
    costs=(
        (4, 0, 0),
        (2, 0, 0),
        (3, 14, 0),
        (2, 0, 7),
    ),
)

example_2 = Blueprint(
    number=1,
    costs=(
        (2, 0, 0),
        (3, 0, 0),
        (3, 8, 0),
        (3, 0, 12),
    ),
)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    blueprints = [Blueprint.parse(line) for line in reader.file_to_lines(19)]
    # blueprints = [example]
    logger.info(f"{blueprints[:3]=}")
    res_1 = sum(
        i * max_geode(blueprint, 24) for i, blueprint in enumerate(blueprints, start=1)
    )
    logger.info(f"{res_1=}")

    res_2 = (
        max_geode(blueprints[0], 32)
        * max_geode(blueprints[1], 32)
        * max_geode(blueprints[2], 32)
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
