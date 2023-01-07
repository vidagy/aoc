#!python3

import logging
from argparse import ArgumentParser, Namespace

from aoc.registry import run

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--log-level", default="INFO", choices=LOG_LEVELS)
    parser.add_argument("-y", "--year", default=None, type=int, required=False)
    parser.add_argument("-d", "--day", default=None, type=int, required=False)
    return parser.parse_args()


def set_logging(log_level: str):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
    )


if __name__ == "__main__":
    args = get_args()
    set_logging(args.log_level)
    run(args.year, args.day)
