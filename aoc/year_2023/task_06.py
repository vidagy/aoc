import logging
from dataclasses import dataclass
from math import ceil, floor, prod, sqrt

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader

logger = logging.getLogger(__name__)


@dataclass
class Race:
    time: int
    distance: int

    @staticmethod
    def load(raw_time: str, raw_dist: str) -> list["Race"]:
        times = [int(t) for t in raw_time.split(":")[1].split()]
        distances = [int(d) for d in raw_dist.split(":")[1].split()]

        return [Race(t, d) for t, d in zip(times, distances)]

    def count_that_beats(self) -> int:
        beats = 0
        for t in range(1, self.time + 1):
            distance = (self.time - t) * t
            if distance > self.distance:
                beats += 1
        return beats

    def count_that_beats_2(self) -> int:
        def d(t: int) -> int:
            return t * (self.time - t)

        lower_t = ceil(
            (self.time - sqrt(self.time * self.time - 4 * self.distance)) / 2
        )
        upper_t = floor(
            (self.time + sqrt(self.time * self.time - 4 * self.distance)) / 2
        )

        return (
            upper_t
            - lower_t
            - 1
            + int(d(lower_t) > self.distance)
            + int(d(upper_t) > self.distance)
        )


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_time, raw_dist = reader.file_to_lines(6)

    races = Race.load(raw_time, raw_dist)
    logger.info(f"{races=}")

    res_1 = prod(race.count_that_beats_2() for race in races)
    logger.info(f"{res_1=}")

    mega_race = Race(
        int("".join([str(race.time) for race in races])),
        int("".join([str(race.distance) for race in races])),
    )
    logger.info(f"{mega_race=}")
    res_2 = mega_race.count_that_beats_2()
    logger.info(f"{res_2=}")

    return res_1, res_2
