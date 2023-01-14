import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


def count_uniques(lines: list[list[str]]) -> int:
    return sum(1 for line in lines for num in line if len(num) in [2, 3, 4, 7])


class Decoder:
    def _save(self, d: str, dd: int) -> None:
        self.decode_map[frozenset(d)] = dd
        self.encode_map[dd] = frozenset(d)

    def __init__(self, digits: list[str]) -> None:
        self.decode_map: dict[frozenset, int] = {}
        self.encode_map: dict[int, frozenset] = {}

        # uniques
        for d in digits:
            if len(d) == 2:
                self._save(d, 1)
            if len(d) == 3:
                self._save(d, 7)
            if len(d) == 4:
                self._save(d, 4)
            if len(d) == 7:
                self._save(d, 8)

        for d in digits:
            dd = frozenset(d)
            if (
                len(dd) == 6
                and dd.issuperset(self.encode_map[1])
                and dd.issuperset(self.encode_map[4])
            ):
                self._save(d, 9)
            if (
                len(dd) == 5
                and dd.issuperset(self.encode_map[1])
                and not dd.issuperset(self.encode_map[4])
            ):
                self._save(d, 3)
            if (
                len(dd) == 6
                and dd.issuperset(self.encode_map[1])
                and not dd.issuperset(self.encode_map[4])
            ):
                self._save(d, 0)

        for d in digits:
            if (
                len(d) == 6
                and frozenset(d) != self.encode_map[9]
                and frozenset(d) != self.encode_map[0]
            ):
                self._save(d, 6)

        for d in digits:
            dd = frozenset(d)
            if dd.issubset(self.encode_map[6]) and len(dd) == 5:
                self._save(d, 5)
            if (
                not dd.issubset(self.encode_map[6])
                and len(dd) == 5
                and frozenset(d) != self.encode_map[3]
            ):
                self._save(d, 2)

        assert len(self.encode_map) == 10, f"{self.encode_map=}"
        assert len(self.decode_map) == 10, f"{self.decode_map=}"

    def decode(self, what: list[str]) -> int:
        num = 0
        for d, digit in enumerate(what[::-1]):
            val = self.decode_map[frozenset(digit)]
            num += (10**d) * val
        return num


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = [
        tuple(p.split(" ") for p in line.split(" | "))
        for line in reader.file_to_lines(8)
    ]
    logger.info(f"{lines[:3]=}...")

    res_1 = count_uniques([o for _, o in lines])
    logger.info(f"{res_1=}")

    res_2 = sum(Decoder(left).decode(right) for left, right in lines)
    logger.info(f"{res_2=}")

    return res_1, res_2
