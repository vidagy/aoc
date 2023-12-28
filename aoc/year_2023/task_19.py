import logging
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

import networkx as nx

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


class Result(Enum):
    R = "R"
    A = "A"


class ConditionalType(Enum):
    Greater = ">"
    Less = "<"


class GearCategory(Enum):
    X = "x"
    M = "m"
    A = "a"
    S = "s"


@dataclass(frozen=True, unsafe_hash=True)
class Gear:
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def create(line: str) -> "Gear":
        return eval(f"Gear({line.strip('{}')})")


Rule = Callable[[Gear], Optional[str]]


@dataclass(frozen=True, unsafe_hash=True)
class ParametricRule(ABC):
    result: str


@dataclass(frozen=True, unsafe_hash=True)
class ConditionalParametricRule(ParametricRule):
    parameter: GearCategory
    conditional: ConditionalType
    value: int

    @staticmethod
    def create(raw: str) -> "ConditionalParametricRule":
        expr, label = raw.split(":")
        cond = "<" if "<" in expr else ">"
        param, value = expr.split(cond)
        return ConditionalParametricRule(
            result=label,
            parameter=GearCategory(param),
            conditional=ConditionalType(cond),
            value=int(value),
        )


@dataclass(frozen=True, unsafe_hash=True)
class UnconditionalParametricRule(ParametricRule):
    pass

    @staticmethod
    def create(raw: str) -> "UnconditionalParametricRule":
        return UnconditionalParametricRule(result=raw)


@dataclass(frozen=True)
class GearRange:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]
    is_positive: bool

    @property
    def deg_freedom(self) -> int:
        return (
            (self.x[1] - self.x[0])
            * (self.m[1] - self.m[0])
            * (self.a[1] - self.a[0])
            * (self.s[1] - self.s[0])
            * (1 if self.is_positive else -1)
        )

    def __hash__(self) -> int:
        return hash((self.x, self.m, self.a, self.s, self.is_positive))

    def __eq__(self, other) -> bool:
        if not isinstance(other, GearRange):
            return False
        return (
            self.x == other.x
            and self.m == other.m
            and self.a == other.a
            and self.s == other.s
            and self.is_positive == other.is_positive
        )

    def copy_with(
        self,
        x: Optional[tuple[int, int]] = None,
        m: Optional[tuple[int, int]] = None,
        a: Optional[tuple[int, int]] = None,
        s: Optional[tuple[int, int]] = None,
    ) -> "GearRange":
        if x is not None:
            return GearRange(x, self.m, self.a, self.s, True)
        if m is not None:
            return GearRange(self.x, m, self.a, self.s, True)
        if a is not None:
            return GearRange(self.x, self.m, a, self.s, True)
        if s is not None:
            return GearRange(self.x, self.m, self.a, s, True)
        return self

    def minus(self, other: "GearRange") -> list["GearRange"]:
        if self.is_positive != other.is_positive:
            return [self]
        if not (
            GearRange.has_overlap(self.x, other.x)
            and GearRange.has_overlap(self.m, other.m)
            and GearRange.has_overlap(self.a, other.a)
            and GearRange.has_overlap(self.s, other.s)
        ):
            return [self]
        res = []

        xx = [self.x] + GearRange.range_minus(self.x, other.x)
        mm = [self.m] + GearRange.range_minus(self.m, other.m)
        aa = [self.a] + GearRange.range_minus(self.a, other.a)
        ss = [self.s] + GearRange.range_minus(self.s, other.s)

        for i, x in enumerate(xx):
            for j, m in enumerate(mm):
                for k, a in enumerate(aa):
                    for n, s in enumerate(ss):
                        if i + j + k + n != 0:
                            is_positive = (
                                int(i != 0) + int(j != 0) + int(k != 0) + int(n != 0)
                            ) % 2
                            res.append(GearRange(x, m, a, s, bool(is_positive)))
        return res

    @staticmethod
    def range_minus(
        this: tuple[int, int], that: tuple[int, int]
    ) -> list[tuple[int, int]]:
        this_s, this_e = this
        that_s, that_e = that
        if that_s <= this_s and that_e >= this_e:
            return []
        if this_s < that_s and that_e >= this_e:
            return [(this_s, that_s)]
        if that_s <= this_s and this_e >= that_e:
            return [(that_e, this_e)]
        if this_s < that_s and that_e < this_e:
            return [(this_s, that_s), (that_e, this_e)]
        raise Exception("fuck")

    @staticmethod
    def has_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
        s_1, e_1 = r1
        s_2, e_2 = r2
        return (s_2 < e_1 <= e_2) or (s_1 < e_2 <= e_1)


@dataclass(frozen=True, unsafe_hash=True)
class Workflow:
    workflow_id: str
    rules: tuple[Rule]
    parametric_rules: tuple[ParametricRule]

    @staticmethod
    def create(line: str) -> "Workflow":
        label, rules_in_one = line.strip("}").split("{")
        raw_rules = rules_in_one.split(",")

        rules: list[Rule] = []
        parametric_rules: list[ParametricRule] = []
        for raw_rule in raw_rules:
            if ":" in raw_rule:
                criteria, lbl = raw_rule.split(":")
                rules.append(eval(f"lambda this: '{lbl}' if this.{criteria} else None"))
                parametric_rules.append(ConditionalParametricRule.create(raw_rule))
            else:
                rules.append(lambda _: raw_rule)
                parametric_rules.append(UnconditionalParametricRule.create(raw_rule))
        return Workflow(label, tuple(rules), tuple(parametric_rules))  # type: ignore

    def __call__(self, gear: Gear) -> str:
        for rule in self.rules:
            res = rule(gear)
            if res:
                return res
        raise Exception("Nope")

    def map_input(self, gear_range: GearRange) -> dict[str, list[GearRange]]:
        res: dict[str, list[GearRange]] = defaultdict(list)

        remainder = gear_range
        for pr in self.parametric_rules:
            if isinstance(pr, UnconditionalParametricRule):
                res[pr.result].append(remainder)
                break
            elif isinstance(pr, ConditionalParametricRule):
                lo, hi = eval(f"remainder.{pr.parameter.value}")
                if (pr.value < lo and pr.conditional == ConditionalType.Greater) or (
                    pr.value >= hi and pr.conditional == ConditionalType.Less
                ):
                    res[pr.result].append(remainder)
                    break
                elif (pr.value <= lo and pr.conditional == ConditionalType.Less) or (
                    pr.value > hi and pr.conditional == ConditionalType.Greater
                ):
                    continue
                else:
                    if pr.conditional == ConditionalType.Less:
                        res[pr.result].append(
                            eval(
                                f"remainder.copy_with({pr.parameter.value}=(lo, pr.value))"
                            )
                        )
                        remainder = eval(
                            f"remainder.copy_with({pr.parameter.value}=(pr.value, hi))"
                        )
                    else:
                        res[pr.result].append(
                            eval(
                                f"remainder.copy_with({pr.parameter.value}=(pr.value + 1, hi))"
                            )
                        )
                        remainder = eval(
                            f"remainder.copy_with({pr.parameter.value}=(lo, pr.value + 1))"
                        )
        return res


def process_gears(
    gears: list[Gear], workflows: dict[str, Workflow]
) -> dict[Gear, Result]:
    res: dict[Gear, Result] = {}
    for _, gear in enumerate(gears):
        wf_id = "in"
        while True:
            if wf_id == "R" or wf_id == "A":
                break
            wf = workflows[wf_id]
            wf_id = wf(gear)
        res[gear] = Result(wf_id)
    return res


def build_workflow_graph_skeleton(workflows: dict[str, Workflow]) -> nx.DiGraph:
    res = nx.DiGraph()

    agg: set[Workflow] = {workflows["in"]}
    done: set[Workflow] = set()
    while agg:
        w = agg.pop()
        if w in done:
            continue
        for pc in w.parametric_rules:
            res.add_edge(w, workflows[pc.result], gear_ranges=[])
            agg.add(workflows[pc.result])
        done.add(w)

    res.add_edge(
        "start",
        workflows["in"],
        gear_ranges=[GearRange((1, 4001), (1, 4001), (1, 4001), (1, 4001), True)],
    )

    return res


def build_workflow_graph(workflows: dict[str, Workflow]) -> nx.DiGraph:
    workflows["A"] = Workflow("A", (), ())  # type: ignore
    workflows["R"] = Workflow("R", (), ())  # type: ignore
    graph = build_workflow_graph_skeleton(workflows)

    for nodes in nx.bfs_layers(graph, workflows["in"]):
        for node in nodes:
            inp_gear_ranges = [
                gear_range
                for _, _, gear_ranges in graph.in_edges(node, data="gear_ranges")
                for gear_range in gear_ranges
            ]
            destinations = defaultdict(list)
            for inp_gr in inp_gear_ranges:
                for dest_label, out_gear_range in node.map_input(inp_gr).items():
                    destinations[dest_label].extend(out_gear_range)

            for label, gear_ranges in destinations.items():
                graph[node][workflows[label]]["gear_ranges"].extend(gear_ranges)

    return graph


def remove_duplicate_ranges(in_ranges: list[GearRange]) -> list[GearRange]:
    res: list[GearRange] = [in_ranges[0]]
    working_set = set(in_ranges)

    while working_set:
        this: Optional[GearRange] = working_set.pop()
        for that in res:
            if this is None:
                break
            residuals = this.minus(that)
            if len(residuals) == 0:
                this = None
                break
            elif len(residuals) > 1:
                working_set.union(residuals[1:])
            this = residuals[0]
        if this is not None:
            res.append(this)

    return res


def calculate_possibilities(graph: nx.DiGraph, workflows: dict[str, Workflow]) -> int:
    in_ranges = []
    for _, _, gear_ranges in graph.in_edges(workflows["A"], data="gear_ranges"):
        in_ranges.extend(gear_ranges)

    orthogonal_ranges = remove_duplicate_ranges(in_ranges)

    return sum(r.deg_freedom for r in orthogonal_ranges)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_rules, raw_gears = split_lines_by_empty_line(reader.file_to_lines(19))

    workflow_list = [Workflow.create(line) for line in raw_rules]
    workflows = {w.workflow_id: w for w in workflow_list}
    gears = [Gear.create(line) for line in raw_gears]

    res_1 = sum(
        g.x + g.m + g.a + g.s
        for g, v in process_gears(gears, workflows).items()
        if v == Result.A
    )
    logger.info(f"{res_1=}")

    workflow_graph = build_workflow_graph(workflows)

    res_2 = calculate_possibilities(workflow_graph, workflows)
    logger.info(f"{res_2=}")

    return res_1, res_2
