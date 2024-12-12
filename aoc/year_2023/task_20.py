import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize
from abc import abstractmethod
from typing import Optional
from networkx import DiGraph
import networkx as nx
from dataclasses import dataclass, field
from collections import deque
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)


@dataclass
class Module:
    label: str

    @abstractmethod
    def __call__(self, is_high: bool, _: str) -> Optional[bool]:
        pass


@dataclass
class FlipFlop(Module):
    is_on: bool = field(default=False)

    def __call__(self, is_high: bool, _: str) -> Optional[bool]:
        if is_high:
            return None
        else:
            self.is_on = not self.is_on
            return self.is_on

    def __repr__(self) -> str:
        return f"%{self.label}[{'+' if self.is_on else '-'}]"


@dataclass(init=False)
class Conjunction(Module):
    def __init__(self, label: str, in_labels: set[str]) -> None:
        super().__init__(label)
        self.is_high = {k: False for k in in_labels}

    def __call__(self, is_high: bool, label: str) -> Optional[bool]:
        self.is_high[label] = is_high
        return not all(self.is_high)

    def __repr__(self) -> str:
        status = "".join(
            '+' if v else '-' for v in self.is_high.values()
        )
        return f"&{self.label}[{status}]"


@dataclass
class Broadcast(Module):
    def __call__(self, is_high: bool, _: str) -> Optional[bool]:
        return is_high

    def __repr__(self) -> str:
        return f"%{self.label}"


@dataclass
class Sink(Module):
    def __call__(self, is_high: bool, _: str) -> Optional[bool]:
        return None

    def __repr__(self) -> str:
        return f"%{self.label}"


class Network:
    def __init__(self, lines: list[str]) -> None:
        tokens = tokenize(lines, separator="->")
        self.graph = self._get_graph(tokens)
        self._add_modules(tokens)

    @staticmethod
    def _label_to_module(label: str, in_labels: set[str]) -> Module:
        if label == "broadcaster":
            return Broadcast(label)
        elif label.startswith("%"):
            return FlipFlop(label[1:])
        elif label.startswith("&"):
            return Conjunction(label[1:], in_labels)
        raise Exception("wtf")

    @staticmethod
    def _get_graph(tokens: list[list[str]]) -> DiGraph:
        res = DiGraph()
        for source, destinations in tokens:
            s = source.strip()
            s = s if s == "broadcaster" else s[1:]
            for dest in destinations.split(","):
                d = dest.strip()
                res.add_edge(s, d)
        return res

    def _add_modules(self, tokens: list[list[str]]) -> None:
        graph = self.graph
        label_to_node_inp = {
            (l if l == "broadcaster" else l[1:]): l for l, _ in tokens
        }
        for label, node_inp in label_to_node_inp.items():
            graph.nodes[label]["module"] = self._label_to_module(
                node_inp, {s for s,_ in graph.in_edges(label)}
            )
        self.graph.nodes["rx"]["module"] = Sink("rx")


def push_button(network: Network) -> tuple[int, int]:
    num_high = 0
    num_low = 0
    graph = network.graph

    to_visit = deque()
    to_visit.append(("button", False, graph.nodes["broadcaster"]["module"]))
    while to_visit:
        from_label, is_high, module = to_visit.popleft()

        if is_high:
            num_high += 1
        else:
            num_low += 1

        new_is_high = module(is_high, from_label)
        logger.info(f"n={len(to_visit)} {from_label} -> {module.label} {is_high} -> {new_is_high}")

        if (num_low + num_high) > 10:
            break
        if new_is_high is not None:
            for s, d in graph.out_edges(module.label):
                to_visit.append((s, new_is_high, graph.nodes[d]["module"]))

    return num_high, num_low


def push_button_1000_times(network: Network) -> int:
    num_high = 0
    num_low = 0
    for i in range(1):
        logger.info(f"{i=}")
        h, l = push_button(network)
        num_high += h
        num_low += l
    return num_low * num_high


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(20)
    logger.info(f"{lines[:3]=}...")

    network = Network(lines)
    relevant_nodes = {n for n in nx.ancestors(network.graph, "rx")}
    graph = nx.subgraph_view(network.graph, filter_node=lambda n: n in relevant_nodes)
    pos = nx.planar_layout(network.graph)
    nx.draw(network.graph, pos=pos, with_labels=True)
    plt.savefig("graph.png")

    logger.info(f"{graph}")
    logger.info(f"{network.graph} ")
    for _, m in network.graph.nodes(data="module"):
        logger.info(f"{m}")

    res_1 = 0 # push_button_1000_times(network)
    logger.info(f"{res_1=}")

    res_2 = 0
    logger.info(f"{res_2=}")

    return res_1, res_2
