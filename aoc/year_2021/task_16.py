import logging
from abc import abstractmethod
from dataclasses import dataclass
from math import prod

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass(frozen=True, unsafe_hash=True)
class Packet:
    version: int
    type_id: int

    @abstractmethod
    def value(self) -> int:
        pass

    @abstractmethod
    def sum_version(self) -> int:
        pass

    @staticmethod
    def create_from_stream(line: str) -> tuple["Packet", str]:
        version = int(line[0:3], 2)
        type_id = int(line[3:6], 2)

        if type_id == 4:
            return Literal.create(version, type_id, line[6:])

        return Operator.create(version, type_id, line[6:])


@dataclass(frozen=True, unsafe_hash=True)
class Literal(Packet):
    number: int

    def value(self) -> int:
        return self.number

    def sum_version(self) -> int:
        return self.version

    @staticmethod
    def create(version: int, type_id: int, line: str) -> tuple["Packet", str]:
        number_str = ""
        index = 0
        for index in range(0, len(line), 5):
            number_str += line[index + 1 : index + 5]
            if line[index] == "0":
                break

        return (
            Literal(version=version, type_id=type_id, number=int(number_str, 2)),
            line[index + 5 :],
        )


@dataclass(frozen=True, unsafe_hash=True)
class Operator(Packet):
    length_type: int
    members: list[Packet]

    def value(self) -> int:
        if self.type_id == 0:
            return sum(m.value() for m in self.members)
        if self.type_id == 1:
            return prod(m.value() for m in self.members)
        if self.type_id == 2:
            return min(m.value() for m in self.members)
        if self.type_id == 3:
            return max(m.value() for m in self.members)
        if self.type_id == 5:
            return int(self.members[0].value() > self.members[1].value())
        if self.type_id == 6:
            return int(self.members[0].value() < self.members[1].value())
        if self.type_id == 7:
            return int(self.members[0].value() == self.members[1].value())

        raise Exception("not implemented")

    def sum_version(self) -> int:
        return self.version + sum(m.sum_version() for m in self.members)

    @staticmethod
    def create(version: int, type_id: int, line: str) -> tuple["Packet", str]:
        length_type = int(line[0], 2)
        members: list[Packet] = []

        if length_type == 0:
            length_in_bits = int(line[1:16], 2)
            starting_line = line[16:]
            original_length = len(starting_line)

            while original_length - len(starting_line) < length_in_bits:
                m, starting_line = Packet.create_from_stream(starting_line)
                members.append(m)
        else:
            length_in_count = int(line[1:12], 2)
            starting_line = line[12:]

            for i in range(length_in_count):
                m, starting_line = Packet.create_from_stream(starting_line)
                members.append(m)

        return (
            Operator(
                version=version,
                type_id=type_id,
                length_type=length_type,
                members=members,
            ),
            starting_line,
        )


def parse_line_2(line: str) -> str:
    res = ""
    for c in line:
        res += "{0:04b}".format(int(c, 16))

    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    inp = reader.file_to_lines(16)[0]
    line = parse_line_2(inp)
    # logger.info(f"{line=}")

    packet, _ = Packet.create_from_stream(line)
    # logger.info(f"{packet=}")

    res_1 = packet.sum_version()
    logger.info(f"{res_1=}")

    res_2 = packet.value()
    logger.info(f"{res_2=}")

    return res_1, res_2
