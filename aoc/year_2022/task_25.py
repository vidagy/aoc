import logging
from dataclasses import dataclass

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass(frozen=True, unsafe_hash=True)
class Snafu:
    num: str

    def __repr__(self) -> str:
        return f"{self.num}"

    def to_decimal(self) -> int:
        res = 0
        for n, digit in enumerate(self.num[::-1]):
            res += (5**n) * self._convert_snafu_to_digit(digit)

        return res

    @staticmethod
    def _to_5_base(n: int) -> list[int]:
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % 5))
            n //= 5
        return digits[::-1]

    @staticmethod
    def from_decimal(num: int) -> "Snafu":
        five_base = Snafu._to_5_base(num)
        snafu_digits = Snafu._to_snafu_digits(five_base)
        snafu_num = "".join([Snafu._convert_digit_to_snafu(d) for d in snafu_digits])
        return Snafu(snafu_num)

    @staticmethod
    def _to_snafu_digits(digits: list[int]) -> list[int]:
        res: list[int] = []
        remainder = 0
        for digit in digits[::-1]:
            new_digit = remainder + digit
            if -2 <= new_digit <= 2:
                res.insert(0, new_digit)
                remainder = 0
            elif new_digit > 2:
                res.insert(0, new_digit - 5)
                remainder = 1
            else:
                raise Exception("not implemented")

        if remainder != 0:
            res.insert(0, remainder)

        return res

    @staticmethod
    def _convert_snafu_to_digit(digit: str) -> int:
        if digit.isnumeric():
            return int(digit)
        elif digit == "-":
            return -1
        elif digit == "=":
            return -2
        else:
            raise Exception(f"not implemented {digit}")

    @staticmethod
    def _convert_digit_to_snafu(digit: int) -> str:
        if 0 <= digit <= 2:
            return str(digit)
        elif digit == -1:
            return "-"
        elif digit == -2:
            return "="
        else:
            raise Exception(f"not implemented {digit}")


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[str, int]:
    snafu_numbers = [Snafu(num) for num in reader.file_to_lines(25)]

    res_1 = Snafu.from_decimal(sum(s.to_decimal() for s in snafu_numbers))
    logger.info(f"{res_1=}")

    return res_1.num, 0
