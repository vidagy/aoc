import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


@dataclass
class Monkey:
    number: int
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], int]

    num_inspections = 0

    def __repr__(self) -> str:
        return f"Monkey({self.number=}, {self.items=})"


def parse_monkey(lines: list[str]) -> Monkey:
    assert len(lines) == 6

    number = int(lines[0].strip(":").split()[1])

    items = [int(item.strip()) for item in lines[1].split(":")[1].split(",")]

    op = lines[2].split("=")[1].strip().split(" ")[1]
    op_num = lines[2].split("=")[1].strip().split(" ")[2]

    def operation(old: int) -> int:
        if op_num == "old":
            nop_num = old
        else:
            nop_num = int(op_num)

        if op == "+":
            return old + nop_num
        elif op == "*":
            return old * nop_num
        raise Exception("Not implemented op")

    divis = int(lines[3].split("by")[1].strip())
    true_monk = int(lines[4].split("monkey")[1].strip())
    false_monk = int(lines[5].split("monkey")[1].strip())

    def test(num: int) -> int:
        return true_monk if num % divis == 0 else false_monk

    logger.info(
        "parsed Monkey("
        f"{number=}, "
        f"{items=}, "
        f'operation="new = old {op} {op_num}", '
        f'test="{true_monk} if num % {divis} == 0 else {false_monk}"'
        ")"
    )

    return Monkey(
        number=number,
        items=items,
        operation=operation,
        test=test,
    )


def decreese_num(worry: int, worry_div: int) -> int:
    if worry_div != 1:
        return worry // worry_div
    elif worry_div == 1:
        worry = worry % (2 * 3 * 5 * 7 * 11 * 13 * 17 * 19)
    return worry


def play_item(
    worry: int, monkey: Monkey, monkeys: list[Monkey], worry_div: int
) -> None:
    monkey.num_inspections += 1
    new_worry = monkey.operation(worry)
    new_worry = decreese_num(new_worry, worry_div)
    new_monkey = monkey.test(new_worry)
    monkeys[new_monkey].items.append(new_worry)

    # logger.info(f" - -> monkey={monkey.number} {worry=} {new_worry=} {new_monkey=}")


def play_monkey(monkey: Monkey, monkeys: list[Monkey], worry_div: int) -> None:
    # logger.info(f" -> monkey={monkey.number} items={monkey.items}")
    while monkey.items:
        item = monkey.items.pop(0)
        play_item(item, monkey, monkeys, worry_div)


def play_round(i: int, monkeys: list[Monkey], worry_div: int) -> None:
    # logger.info(f"round={i} {monkeys=}")
    for monkey in monkeys:
        play_monkey(monkey, monkeys, worry_div)


def get_result(monkeys: list[Monkey], num_rounds: int, worry_div: int) -> int:
    for i in range(num_rounds):
        play_round(i, monkeys, worry_div)

    inspections = sorted([m.num_inspections for m in monkeys])
    # logger.info(f"{inspections=}")

    return inspections[-1] * inspections[-2]


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = split_lines_by_empty_line(reader.file_to_lines(11))
    monkeys = [parse_monkey(monkey_def) for monkey_def in lines]

    res_1 = get_result(deepcopy(monkeys), num_rounds=20, worry_div=3)
    logger.info(f"{res_1=}")

    res_2 = get_result(deepcopy(monkeys), num_rounds=10000, worry_div=1)
    logger.info(f"{res_2=}")

    return res_1, res_2
