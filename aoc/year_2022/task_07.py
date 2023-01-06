import logging
from dataclasses import dataclass
from typing import Optional

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass
class File:
    name: str
    size: int

    def __repr__(self) -> str:
        return f"{self.name}({self.size})"


@dataclass
class Dir:
    name: str
    dirs: list["Dir"]
    files: list[File]
    parent: Optional["Dir"]
    size: int = 0

    def __repr__(self) -> str:
        return f"{self.name}({self.size}) -> [ {self.dirs} {self.files} ]"


def parse_line(line: str, current_dir: Dir) -> Dir:
    if not line:
        return current_dir
    elif line == "$ cd ..":
        if current_dir.parent is None:
            raise Exception("invalild input")
        return current_dir.parent
    elif line.startswith("$ cd "):
        subdir_name = line.replace("$ cd ", "")
        subdir = [dir for dir in current_dir.dirs if dir.name == subdir_name][0]
        return subdir
    elif line.startswith("$ ls"):
        return current_dir
    elif line.startswith("dir "):
        subdir = Dir(line.replace("dir ", ""), [], [], current_dir)
        current_dir.dirs.append(subdir)
        return current_dir
    else:
        [size, name] = line.split()
        current_dir.files.append(File(name, int(size)))
        return current_dir


def parse_input(lines: list[str]) -> Dir:
    root = Dir("/", [], [], None)
    current_dir = root
    for line in lines[1:]:
        current_dir = parse_line(line, current_dir)

    return root


def calculate_size(root: Dir) -> None:
    for d in root.dirs:
        calculate_size(d)
    root.size = sum([d.size for d in root.dirs] + [f.size for f in root.files])
    return


def get_res_1(subsum: int, root: Dir) -> int:
    for d in root.dirs:
        subsum = get_res_1(subsum, d)
    if root.size <= 100000:
        subsum += root.size
    return subsum


def find_min_dir_size_greater(root: Dir, space_needed: int, smallest) -> int:
    for d in root.dirs:
        smallest = find_min_dir_size_greater(d, space_needed, smallest)
    if root.size >= space_needed and root.size < smallest:
        smallest = root.size
    return smallest


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(7)
    logger.info(f"{lines[:3]=}...")

    root = parse_input(lines)
    calculate_size(root)
    logger.info(f"{root=}")

    res_1, res_2 = 0, root.size
    res_1 = get_res_1(res_1, root)
    logger.info(f"{res_1=}")

    space_available = 70000000 - root.size
    space_needed = 30000000 - space_available
    logger.info(f"{space_available=}")
    logger.info(f"{space_needed=}")

    res_2 = find_min_dir_size_greater(root, space_needed, res_2)
    logger.info(f"{res_2=}")

    return res_1, res_2
