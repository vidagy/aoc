import logging
import re
from pathlib import Path

from requests import get, post

logger = logging.getLogger(__name__)


def get_cookies() -> dict[str, str]:
    path = Path(__file__).parent.parent.parent / "session.cookie"
    with open(path, mode="r") as f:
        session = f.readlines()[0].strip()
    return {"session": session}


def get_task_input(year: int, day: int) -> bytes:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    resp = get(url, cookies=get_cookies())
    if resp.status_code != 200:
        raise Exception("Failed to fetch input data")
    return resp.content


def submit(year: int, day: int, part: int, res: str) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {"level": part, "answer": res}
    logger.info(f"Submitting {data} for {year=} {day=}...")
    resp = post(url, data=data, cookies=get_cookies())
    if resp.status_code != 200:
        raise Exception(f"Failed to submit solution {resp=}")

    text_content = resp.content.decode("utf-8")

    if "That's the right answer!" in text_content:
        logger.info("Correct answer, nice!")
        return

    if "Did you already complete it?" in text_content:
        logger.info("Correct solution already submitted.")
        return

    time_out_min = 0
    time_out_sec = 0

    if "That's not the right answer." in text_content:
        if "wait one minute before trying again" in text_content:
            time_out_min = 1
        if "wait 5 minutes before trying again" in text_content:
            time_out_min = 5

        logger.info(f"Wrong answer, please attempt again after {time_out_min}m.")
        return

    if "You gave an answer too recently" in text_content:
        rex = r"You have (([\d]+)m )?([\d]+)s left to wait"
        groups = re.findall(rex, text_content)
        if groups and groups[0]:
            time_out_min = int(groups[0][1]) if groups[0][1] else 0
            time_out_sec = int(groups[0][2])

        logger.info(
            f"Wait some more... try again after {time_out_min}m {time_out_sec}s."
        )
        return
