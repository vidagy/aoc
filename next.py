#!python3

import os
import re
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from datetime import date
from pathlib import Path

from requests import get

TEMPLATE = """import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(1)
    logger.info(f"{lines[:3]=}...")

    return 0, 0
"""

TEST_TEMPLATE = """from aoc.registry import SolutionRegistry

"""

TEST_CASE_TEMPLATE = """
def test_task_%(day)02d():
    res_1, res_2 = SolutionRegistry.run(%(year)s, %(day)s)
    assert res_1 == 0
    assert res_2 == 0
"""


def find_solutions() -> dict[int, set[int]]:
    root_dir = Path(__file__).parent
    files = root_dir.glob("aoc/year_*/task_*.py")
    rex = re.compile(r"year_([0-9]+).*task_([0-9]+)")
    res = defaultdict(set)

    for file in files:
        year, day = rex.findall(str(file))[0]
        res[int(year)].add(int(day))

    return res


def get_max_day(state: dict[int, set[int]]) -> tuple[int, int]:
    if not state:
        return date.today().year, 1
    year = max(state)
    days = state[year]
    if not days:
        return year, 1
    return year, max(days)


def get_new_day(state: dict[int, set[int]]) -> tuple[int, int]:
    year, day = get_max_day(state)
    if day == 25:
        return year + 1, 1
    return year, day + 1


def create_new_year(year_dir: Path, data_dir: Path, test_dir: Path) -> None:
    os.makedirs(year_dir, exist_ok=True)
    (year_dir / "__init__.py").touch()

    os.makedirs(data_dir, exist_ok=True)

    os.makedirs(test_dir, exist_ok=True)
    (test_dir / "__init__.py").touch()
    test_tasks_file = test_dir / "test_task.py"
    with open(test_tasks_file, mode="w") as f:
        f.writelines(TEST_TEMPLATE)


def create_new_day(year_dir: Path, test_dir: Path, year: int, day: int) -> None:
    with open(year_dir / f"task_{day:02d}.py", mode="w") as f:
        f.writelines(TEMPLATE)

    with open(test_dir / "test_task.py", mode="a") as f:
        f.writelines(TEST_CASE_TEMPLATE % {"year": year, "day": day})


def get_session_cookie() -> str:
    path = Path(__file__).parent / "session.cookie"
    with open(path, mode="r") as f:
        return f.readlines()[0].strip()


def get_data(data_dir: Path, year: int, day: int) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    data = get(url, cookies={"session": get_session_cookie()}).content
    with open(data_dir / f"task_{day:02d}.txt", mode="wb") as f:
        f.write(data)


def create_task(year: int, day: int) -> None:
    root_dir = Path(__file__).parent
    year_dir = root_dir / "aoc" / f"year_{year}"
    data_dir = root_dir / "data" / f"{year}"
    test_dir = root_dir / "tests" / "unit" / f"year_{year}"

    if day == 1:
        create_new_year(year_dir, data_dir, test_dir)
    create_new_day(year_dir, test_dir, year, day)
    get_data(data_dir, year, day)


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-y", "--year", default=None, type=int, required=False)
    parser.add_argument("-d", "--day", default=None, type=int, required=False)
    return parser.parse_args()


def main():
    args = get_args()
    current_state = find_solutions()
    new_year, new_day = get_new_day(current_state)

    if args.year is not None:
        new_year = args.year
    if args.day is not None:
        new_day = args.day

    create_task(new_year, new_day)


if __name__ == "__main__":
    main()
