#!/usr/bin/env python3

import logging
import os
import re
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Optional

from aoc.util.integration import get_task_input

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s : %(message)s"
)
logger = logging.getLogger(__name__)

TEMPLATE = """import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(%(day)d)
    logger.info(f"{lines[:3]=}...")

    res_1 = 0
    logger.info(f"{res_1=}")

    res_2 = 0
    logger.info(f"{res_2=}")

    return res_1, res_2
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


def get_max_day(
    state: dict[int, set[int]], year_override: Optional[int]
) -> tuple[int, int]:
    if not state:
        return date.today().year, 1
    year = year_override if year_override is not None else max(state)
    days = state[year]
    if not days:
        return year, 1
    return year, max(days)


def get_new_day(
    state: dict[int, set[int]],
    year_override: Optional[int],
    day_override: Optional[int],
) -> tuple[int, int]:
    if year_override is not None and day_override is not None:
        if year_override in state and day_override in state[year_override]:
            logger.info(
                f"Files already exist, "
                f"will not create them again: "
                f"year={year_override} day={day_override}"
            )
            exit()
        return year_override, day_override

    year, day = get_max_day(state, year_override)
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
        f.writelines(TEMPLATE % {"day": day})

    with open(test_dir / "test_task.py", mode="a") as f:
        f.writelines(TEST_CASE_TEMPLATE % {"year": year, "day": day})


def get_data(data_dir: Path, year: int, day: int) -> None:
    data = get_task_input(year, day)
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
    new_year, new_day = get_new_day(current_state, args.year, args.day)

    create_task(new_year, new_day)


if __name__ == "__main__":
    main()
