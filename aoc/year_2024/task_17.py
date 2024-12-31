import logging
from copy import deepcopy
from dataclasses import dataclass
from re import L
from typing import Any, Callable

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass
class Computer:
    a: int
    b: int
    c: int
    instructions: list[int]
    instr_ptr: int
    just_jumped: bool
    output: list[int]

    @staticmethod
    def create(lines: list[str]) -> "Computer":
        a = int(lines[0].split()[-1])
        b = int(lines[1].split()[-1])
        c = int(lines[2].split()[-1])
        instructions = [int(t) for t in lines[4].split()[-1].split(",")]

        return Computer(
            a, b, c, instructions, instr_ptr=0, just_jumped=False, output=[]
        )

    def __repr__(self):
        return f"{self.a:10d} {self.b:10d} {self.c:10d} {self.instructions}[{self.instr_ptr}]"

    def _combo_op_code_map(self, op_code: int) -> int:
        assert 0 <= op_code < 7

        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.a,
            5: self.b,
            6: self.c,
        }[op_code]

    def _instruction_op_code_map(self, op_code: int) -> Callable[[int], None]:
        return {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }[op_code]

    def adv(self, operand: int) -> None:
        # logger.info(f"{self} adv({pow(2, self._combo_op_code_map(operand))})")
        self.a = self.a // pow(2, self._combo_op_code_map(operand))

    def bxl(self, operand: int) -> None:
        # logger.info(f"{self} bxl({operand})")
        self.b = self.b ^ operand

    def bst(self, operand: int) -> None:
        # logger.info(f"{self} bst({self._combo_op_code_map(operand)})")
        self.b = self._combo_op_code_map(operand) % 8

    def jnz(self, operand: int) -> None:
        # logger.info(f"{self} jnz({operand})")
        if self.a == 0:
            return
        self.instr_ptr = operand
        self.just_jumped = True

    def bxc(self, _: int) -> None:
        # logger.info(f"{self} bxc()")
        self.b = self.b ^ self.c

    def out(self, operand: int) -> None:
        # logger.info(f"{self} out({self._combo_op_code_map(operand) % 8})")
        self.output.append(self._combo_op_code_map(operand) % 8)

    def bdv(self, operand: int) -> None:
        # logger.info(f"{self} bdv({pow(2, self._combo_op_code_map(operand))})")
        self.b = self.a // pow(2, self._combo_op_code_map(operand))

    def cdv(self, operand: int) -> None:
        # logger.info(f"{self} cdv({pow(2, self._combo_op_code_map(operand))})")
        self.c = self.a // pow(2, self._combo_op_code_map(operand))

    def run(self) -> None:
        while self.instr_ptr < len(self.instructions) - 1:
            instruction = self.instructions[self.instr_ptr]
            operand = self.instructions[self.instr_ptr + 1]
            self._instruction_op_code_map(instruction)(operand)

            if self.just_jumped:
                self.just_jumped = False
            else:
                self.instr_ptr += 2

    def prints_itself(self) -> bool:
        a = self.a
        while self.instr_ptr < len(self.instructions) - 1:
            # if  (
            #     self.output and
            #     self.output[-1] != self.instructions[len(self.output) -1]
            # ):
            #     logger.info(f"{a:8d} END! {self} {self.output}")
            #     return False

            instruction = self.instructions[self.instr_ptr]
            operand = self.instructions[self.instr_ptr + 1]
            self._instruction_op_code_map(instruction)(operand)

            if self.just_jumped:
                self.just_jumped = False
            else:
                self.instr_ptr += 2

        # if len(self.output) == len(self.instructions):
        logger.info(f"{a:8d} END! {self} {self.output}")
        return self.output == self.instructions


def find_self(computer: Computer) -> int:
    # min 35184370000000
    # max 281480000000000
    # 2, 4: 64 -> 6
    # 2, 4, 1: 1k -> 10
    # 2, 4, 1, 3: 16k -> 14
    # 2, 4, 1, 3, 7: 1M -> 20
    # 35184380371647
    # 35184380404415
    # 35184380437183
    # 35184380469951
    # 2, 4, 1, 3, 7, 5: 32M -> 25
    for i in range(35184380469951, 281480000000000, 2**20):
        if i % 10000 == 0:
            logger.info(f"{i=}")
        c = Computer(
            a=i,
            b=0,
            c=0,
            instructions=computer.instructions,
            instr_ptr=0,
            just_jumped=False,
            output=[],
        )
        if c.prints_itself():
            return i
    return 0


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[str, int]:
    lines = reader.file_to_lines(17)
    computer = Computer.create(lines)
    logger.info(f"{computer=}")

    computer.run()

    res_1 = ",".join(str(o) for o in computer.output)
    logger.info(f"{res_1=}")

    res_2 = 0  # find_self(computer)
    logger.info(f"{res_2=}")

    return res_1, res_2
