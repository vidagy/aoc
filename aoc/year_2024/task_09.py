import logging
from abc import abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize_by_char

logger = logging.getLogger(__name__)


@dataclass
class Segment:
    length: int

    @abstractmethod
    def value(self, start_pos: int) -> int:
        pass


@dataclass
class File(Segment):
    file_id: int

    def value(self, start_pos: int) -> int:
        return sum(self.file_id * (start_pos + i) for i in range(self.length))


@dataclass
class Space(Segment):
    def value(self, start_pos: int) -> int:
        return 0

    def fill(self, file: File) -> tuple[File, Optional["Space"], Optional[File]]:
        fit = min(file.length, self.length)
        filler = File(fit, file.file_id)
        remainder_space = Space(self.length - fit) if self.length - fit > 0 else None
        remainder_file = (
            File(file.length - fit, file.file_id) if file.length - fit > 0 else None
        )

        return filler, remainder_space, remainder_file


@dataclass
class Drive:
    disk: list[Segment]

    @staticmethod
    def create(line: list[int]) -> "Drive":
        disk: list[Segment] = []
        for i, n in enumerate(line):
            if i % 2 == 0:
                # file
                disk.append(File(n, i // 2))
            else:
                # space
                disk.append(Space(n))
        if isinstance(disk[-1], Space):
            disk = disk[:-1]
        return Drive(disk)

    def defrag(self) -> "Drive":
        res: list[Segment] = []

        reverse = reversed(self.disk[::2])
        leftover_file: Optional[Segment] = next(reverse)
        assert isinstance(leftover_file, File)
        max_split_id: int = leftover_file.file_id

        for segment in self.disk:
            if not segment.length:
                continue
            if isinstance(segment, File):
                if segment.file_id == max_split_id:
                    break
                res.append(segment)
            if isinstance(segment, Space):
                leftover_space: Optional[Space] = segment
                while leftover_space:
                    if not leftover_file:
                        leftover_file = next(reverse)
                        assert isinstance(leftover_file, File)
                        max_split_id = leftover_file.file_id
                    filler, leftover_space, leftover_file = leftover_space.fill(
                        leftover_file
                    )
                    res.append(filler)

        if leftover_file:
            res.append(leftover_file)

        return Drive(res)

    def checksum(self) -> int:
        res = 0
        start_pos = 0
        for segment in self.disk:
            res += segment.value(start_pos)
            start_pos += segment.length
        return res

    def move_files_left(self) -> "Drive":
        res: list[Segment] = deepcopy(self.disk)

        for file in self.disk[::-2]:
            assert isinstance(file, File)
            for i, segment in enumerate(res):
                if isinstance(segment, File):
                    if segment.file_id == file.file_id:
                        break
                    continue
                if isinstance(segment, Space):
                    if file.length <= segment.length:
                        # we can replace
                        filler, leftover_space, _ = segment.fill(file)
                        res = merge_spaces(
                            res[:i]
                            + [filler]
                            + ([leftover_space] if leftover_space else [])
                            + [
                                (
                                    s
                                    if not (
                                        isinstance(s, File)
                                        and s.file_id == file.file_id
                                    )
                                    else Space(s.length)
                                )
                                for s in res[i + 1 :]
                            ]
                        )
                        break

                continue
        return Drive(res)


def merge_spaces(inp: list[Segment]) -> list[Segment]:
    res: list[Segment] = []
    assert len(inp) > 1
    pre = inp[0]
    for s in inp[1:]:
        if isinstance(s, File):
            res.append(pre)
            pre = s
        if isinstance(s, Space):
            if isinstance(pre, File):
                res.append(pre)
                pre = s
            elif isinstance(pre, Space):
                pre = Space(pre.length + s.length)
            continue
    res.append(pre)
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    line = convert(tokenize_by_char(reader.file_to_lines(9)), int)[0]
    logger.info(f"{line[:3]=}...")
    drive = Drive.create(line)

    res_1 = drive.defrag().checksum()
    logger.info(f"{res_1=}")

    res_2 = drive.move_files_left().checksum()
    logger.info(f"{res_2=}")

    return res_1, res_2
