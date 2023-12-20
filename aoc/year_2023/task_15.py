import logging
from dataclasses import dataclass
from enum import Enum

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def elf_hash(input: str) -> int:
    res = 0
    for c in input:
        res += ord(c)
        res *= 17
        res = res % 256
    return res


class Action(Enum):
    Add = "="
    Remove = "-"


@dataclass
class Lens:
    label: str
    focal: int

    @staticmethod
    def parse(input: str) -> tuple["Lens", Action]:
        if "=" in input:
            label, focal = input.split("=")
            return Lens(label, int(focal)), Action.Add
        if "-" in input:
            label = input.strip("-")
            return Lens(label, 0), Action.Remove
        raise Exception("Nope")

    def __eq__(self, other) -> bool:
        return self.label == other.label


@dataclass
class Box:
    lenses: list[Lens]

    def add_lens(self, lens: Lens) -> None:
        if lens in self.lenses:
            index = self.lenses.index(lens)
            self.lenses[index] = lens
        else:
            self.lenses.append(lens)

    def remove_lens(self, lens: Lens) -> None:
        if lens in self.lenses:
            self.lenses.remove(lens)


@dataclass
class InitSeq:
    seq: list[str]

    def arrange_boxes(self) -> list[Box]:
        res = [Box([]) for i in range(256)]
        for instruction in self.seq:
            lens, action = Lens.parse(instruction)
            e_hash = elf_hash(lens.label)
            if action == Action.Add:
                res[e_hash].add_lens(lens)
            if action == Action.Remove:
                res[e_hash].remove_lens(lens)

        return res


def score_boxes(boxes: list[Box]) -> int:
    res = 0
    for i, box in enumerate(boxes, start=1):
        for j, lens in enumerate(box.lenses, start=1):
            res += i * j * lens.focal
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    line = reader.file_to_lines(15)[0]

    init_seq = InitSeq(line.split(","))

    res_1 = sum(elf_hash(s) for s in init_seq.seq)
    logger.info(f"{res_1=}")

    res_2 = score_boxes(init_seq.arrange_boxes())
    logger.info(f"{res_2=}")

    return res_1, res_2
