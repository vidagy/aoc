import logging
from collections import deque

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


SCORES = {"": 0, ")": 3, "]": 57, "}": 1197, ">": 25137}
ENDING_SCORES = {"(": 1, "[": 2, "{": 3, "<": 4}


def get_offending_char(line: str) -> str:
    stack: deque[str] = deque()
    for c in line:
        if c in {"(", "[", "{", "<"}:
            stack.append(c)
        if c in {")", "]", "}", ">"}:
            prev = stack.pop()
            if c == ")":
                if prev != "(":
                    return c
            elif c == "]":
                if prev != "[":
                    return c
            elif c == "}":
                if prev != "{":
                    return c
            elif c == ">":
                if prev != "<":
                    return c
    return ""


def complete_and_score(line: str) -> int:
    stack: deque[str] = deque()
    for c in line:
        if c in {"(", "[", "{", "<"}:
            stack.append(c)
        if c in {")", "]", "}", ">"}:
            stack.pop()

    score = 0
    while stack:
        score *= 5
        score += ENDING_SCORES[stack.pop()]
    return score


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(10)
    logger.info(f"{lines[:3]=}...")

    validated_lines = [(line, get_offending_char(line)) for line in lines]

    res_1 = sum(SCORES[oc] for _, oc in validated_lines)
    logger.info(f"{res_1=}")

    scores = sorted(
        [complete_and_score(line) for line, oc in validated_lines if oc == ""]
    )
    res_2 = scores[len(scores) // 2]
    logger.info(f"{res_2=}")

    return res_1, res_2
