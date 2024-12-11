import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


class Expression:
    def __init__(self, line: str) -> None:
        raw_res, raw_args = line.split(":")

        self.res = int(raw_res)
        self.args = [int(n.strip()) for n in raw_args.strip().split()]

        assert len(self.args) > 1

    def __repr__(self):
        return f"{self.res}: {self.args}"

    def possible(self, with_concatenation: bool = False) -> bool:
        return Expression.is_possible(
            self.res, self.args[0], self.args[1:], with_concatenation
        )

    @staticmethod
    def is_possible(
        res: int, head: int, tail: list[int], with_concatenation: bool = False
    ) -> bool:
        # stopping condition
        if not tail:
            return res == head

        # dynamic statement
        return (
            Expression.is_possible(res, head + tail[0], tail[1:], with_concatenation)
            or Expression.is_possible(res, head * tail[0], tail[1:], with_concatenation)
            or (
                with_concatenation
                and Expression.is_possible(
                    res, int(str(head) + str(tail[0])), tail[1:], with_concatenation
                )
            )
        )


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = [Expression(line) for line in reader.file_to_lines(7)]
    logger.info(f"{lines[:3]=}...")

    res_1 = sum(expression.res for expression in lines if expression.possible())
    logger.info(f"{res_1=}")

    res_2 = sum(
        expression.res
        for expression in lines
        if expression.possible(with_concatenation=True)
    )
    logger.info(f"{res_2=}")

    return res_1, res_2
