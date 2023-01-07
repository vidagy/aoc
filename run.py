#!python3

import logging
from argparse import ArgumentParser, Namespace

from aoc.registry import run
from aoc.util.integration import submit

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_args() -> Namespace:
    parser = ArgumentParser()
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
    res_1, res_2 = run(args.year, args.day)  # type: ignore

    if args.submit:
        res = str(res_1) if args.submit == 1 else str(res_2)
        submit(args.year, args.day, args.submit, res)
