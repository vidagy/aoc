import logging
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
    logger.info(f"Submitting {data}...")
    resp = post(url, data=data, cookies=get_cookies())
    if resp.status_code != 200:
        raise Exception("Failed to submit solution")

    logger.info("Done")

    logger.debug(f"response is {str(resp.content)}")
