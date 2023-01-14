import logging
from collections import defaultdict

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, tokenize

logger = logging.getLogger(__name__)


def find_paths_from(
    starting_point: str,
    past: list[str],
    edges: dict[str, list[str]],
    res: list[list[str]],
    already_visited_small: bool,
) -> None:
    next_stops = edges[starting_point]
    for next_stop in next_stops:
        current = past + [next_stop]
        if next_stop == "start":
            continue
        if next_stop == "end":
            res.append(current)
            continue
        if next_stop.islower() and next_stop in past:
            if already_visited_small:
                continue
            else:
                find_paths_from(next_stop, current, edges, res, True)
                continue

        find_paths_from(next_stop, current, edges, res, already_visited_small)


def find_all_paths(
    edges: dict[str, list[str]], visit_small_twice: bool
) -> list[list[str]]:
    res: list[list[str]] = []
    find_paths_from(
        "start", ["start"], edges, res, already_visited_small=not visit_small_twice
    )
    return res


def get_edges(lines: list[list[str]]) -> dict[str, list[str]]:
    res: dict[str, list[str]] = defaultdict(list)
    for start, end in lines:
        res[start].append(end)
        res[end].append(start)
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = tokenize(reader.file_to_lines(12), separator="-")
    logger.info(f"{lines[:3]=}...")

    edges = get_edges(lines)

    res_1 = len(find_all_paths(edges, visit_small_twice=False))
    logger.info(f"{res_1=}")

    res_2 = len(find_all_paths(edges, visit_small_twice=True))
    logger.info(f"{res_2=}")

    return res_1, res_2
