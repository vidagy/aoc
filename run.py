#!/usr/bin/env python3.12

import logging
from argparse import ArgumentParser, Namespace

from aoc.registry import SolutionRegistry
from aoc.util.integration import submit

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_args() -> Namespace:
    parser = ArgumentParser(
        description=("Command line utility to run the last task."),
        epilog=(
            "Simple usage is just to call without arguments: "
            '"./run.py". '
            "This will run the last solution."
        ),
    )
    parser.add_argument("--log-level", default="INFO", choices=LOG_LEVELS)
    parser.add_argument("-y", "--year", default=None, type=int, required=False)
    parser.add_argument("-d", "--day", default=None, type=int, required=False)
    parser.add_argument(
        "-s", "--submit", default=None, type=int, required=False, choices=[1, 2]
    )
    return parser.parse_args()


def set_logging(log_level: str):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
    )


if __name__ == "__main__":
    args = get_args()
    set_logging(args.log_level)

    year, day = SolutionRegistry.get_year_date(args.year, args.day)
    res_1, res_2 = SolutionRegistry.run(year, day)  # type: ignore

    if args.submit:
        res = str(res_1) if args.submit == 1 else str(res_2)
        submit(year, day, args.submit, res)
