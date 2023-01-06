import logging
import re
from abc import ABC, abstractmethod
from typing import Optional

from networkx import DiGraph, shortest_simple_paths

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class Monkey(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @abstractmethod
    def get(self, graph: DiGraph) -> int:
        pass


class NumberMonkey(Monkey):
    def __init__(self, name: str, num: int) -> None:
        super().__init__(name)
        self.num = num

    def get(self, graph: DiGraph) -> int:
        return self.num

    def __repr__(self) -> str:
        return f"{self.name}[{self.num}]"

    def set(self, num: int) -> None:
        self.num = num


class RepeaterMonkey(Monkey):
    def __init__(self, name: str, what: str) -> None:
        super().__init__(name)
        self.what = what

    def get(self, graph: DiGraph) -> int:
        what: Monkey = graph.nodes(data=True)[self.what]["monkey"]
        return what.get(graph)

    def __repr__(self) -> str:
        return f"{self.name}[{self.what}]"


class OperationMonkey(Monkey):
    def __init__(self, name: str, raw_op: str, lhs: str, rhs: str) -> None:
        super().__init__(name)
        self.raw_op = raw_op
        self.lhs = lhs
        self.rhs = rhs

    def get(self, graph: DiGraph) -> int:
        lhs: Monkey = graph.nodes(data=True)[self.lhs]["monkey"]
        rhs: Monkey = graph.nodes(data=True)[self.rhs]["monkey"]

        if self.raw_op == "+":
            op = lambda x, y: x + y  # noqa: E731
        elif self.raw_op == "-":
            op = lambda x, y: x - y  # noqa: E731
        elif self.raw_op == "*":
            op = lambda x, y: x * y  # noqa: E731
        elif self.raw_op == "/":
            op = lambda x, y: x / y  # noqa: E731
        else:
            raise Exception("Not implemented")

        return op(lhs.get(graph), rhs.get(graph))

    def __repr__(self) -> str:
        return f"{self.name}[{self.lhs} {self.raw_op} {self.rhs}]"


def parse_line(line: str) -> Monkey:
    reg_number = re.compile(r"([a-z]+): ([0-9]+)")
    reg_op = re.compile(r"([a-z]+): ([a-z]+) ([+\-*/]) ([a-z]+)")
    match_number = reg_number.match(line)
    if match_number:
        return NumberMonkey(match_number.groups()[0], int(match_number.groups()[1]))

    match_op = reg_op.match(line)
    if match_op:
        return OperationMonkey(
            match_op.groups()[0],
            match_op.groups()[2],
            match_op.groups()[1],
            match_op.groups()[3],
        )

    raise Exception("Not implemented")


def build_graph(monkeys: list[Monkey]) -> DiGraph:
    graph = DiGraph()
    for monkey in monkeys:
        graph.add_node(monkey.name, monkey=monkey)

    for monkey in monkeys:
        if isinstance(monkey, OperationMonkey):
            graph.add_edge(monkey.lhs, monkey.name)
            graph.add_edge(monkey.rhs, monkey.name)
        elif isinstance(monkey, RepeaterMonkey):
            graph.add_edge(monkey.what, monkey.name)
    return graph


def get_res_1(graph: DiGraph) -> int:
    root = graph.nodes(data=True)["root"]["monkey"]
    res_1 = root.get(graph)
    return int(res_1)


def inerted_op_monkey(monkey: OperationMonkey, path: set[str]) -> Monkey:
    is_lhs_in_path = monkey.lhs in path
    name = monkey.lhs if is_lhs_in_path else monkey.rhs
    other = monkey.rhs if is_lhs_in_path else monkey.lhs
    if monkey.raw_op == "+":
        return OperationMonkey(name, "-", monkey.name, other)
    elif monkey.raw_op == "*":
        return OperationMonkey(name, "/", monkey.name, other)
    elif monkey.raw_op == "-":
        if is_lhs_in_path:
            return OperationMonkey(name, "+", monkey.name, other)
        else:
            return OperationMonkey(name, "-", other, monkey.name)
    elif monkey.raw_op == "/":
        if is_lhs_in_path:
            return OperationMonkey(name, "*", monkey.name, other)
        else:
            return OperationMonkey(name, "/", other, monkey.name)
    else:
        raise Exception("Not implemented")


def invert(path: list[str], path_set: set[str], monkey: Monkey) -> Optional[Monkey]:
    inverted_monkey: Optional[Monkey] = None
    if monkey.name == "humn":
        assert isinstance(monkey, NumberMonkey)
        inverted_monkey = None
    elif monkey.name == "root":
        assert isinstance(monkey, OperationMonkey)
        other = monkey.lhs if monkey.lhs in path_set else monkey.rhs
        what = monkey.rhs if monkey.lhs in path_set else monkey.lhs
        inverted_monkey = RepeaterMonkey(other, what)
    elif isinstance(monkey, OperationMonkey):
        inverted_monkey = inerted_op_monkey(monkey, path_set)
    else:
        raise Exception("Not implemented")

    # logger.info(f"{monkey=} {inverted_monkey=}")
    return inverted_monkey


def generate_inverted_graph(graph: DiGraph, path: list[str]) -> DiGraph:
    path_set = set(path)
    inverted_monkeys = [
        invert(path, path_set, graph.nodes(data=True)[m]["monkey"])
        for m in graph.nodes
        if m in path_set
    ]
    inverted_monkeys = [m for m in inverted_monkeys if m]
    ok_monkeys = [
        graph.nodes(data=True)[m]["monkey"] for m in graph.nodes if m not in path_set
    ]
    # logger.info(f"{len(ok_monkeys)=} {len(inverted_monkeys)=}")
    return build_graph(ok_monkeys + inverted_monkeys)


def get_res_2(graph: DiGraph) -> int:
    paths = list(shortest_simple_paths(graph, "humn", "root"))
    assert len(paths) == 1
    path = paths[0]
    # logger.info(f"{path=}")

    inverted_graph = generate_inverted_graph(graph, path)
    humn = inverted_graph.nodes(data=True)["humn"]["monkey"]
    res_2 = humn.get(inverted_graph)
    return int(res_2)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = [parse_line(line) for line in reader.file_to_lines(21)]
    logger.info(f"{inp[:3]=}")
    graph = build_graph(inp)

    res_1 = get_res_1(graph)
    logger.info(f"{res_1=}")

    res_2 = get_res_2(graph)
    logger.info(f"{res_2=}")

    # check
    graph.nodes(data=True)["humn"]["monkey"].set(int(res_2))
    root_lhs = graph.nodes(data=True)["root"]["monkey"].lhs
    root_rhs = graph.nodes(data=True)["root"]["monkey"].rhs
    assert graph.nodes(data=True)[root_lhs]["monkey"].get(graph) == graph.nodes(
        data=True
    )[root_rhs]["monkey"].get(graph)

    return res_1, res_2
