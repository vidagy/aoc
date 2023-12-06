import logging
from dataclasses import dataclass
from itertools import islice
from typing import Optional

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line

logger = logging.getLogger(__name__)


T = dict[tuple[int, int], tuple[int, int]]


@dataclass
class TaskInput:
    seeds: list[int]
    seed_to_soil: T
    soil_to_fertilizer: T
    fertilizer_to_water: T
    water_to_light: T
    light_to_temperature: T
    temperature_to_humidity: T
    humidity_to_location: T

    @staticmethod
    def get_mapped(mapping: T, key: int) -> int:
        for (key_start, key_end), (value_start, _) in mapping.items():
            if key_start <= key < key_end:
                return value_start + key - key_start
        return key

    @staticmethod
    def get_intersection(
        s_1: int, e_1: int, s_2: int, e_2: int
    ) -> Optional[tuple[int, int]]:
        if e_1 <= s_2 or e_2 <= s_1:
            return None
        return (max(s_1, s_2), min(e_1, e_2))

    @staticmethod
    def find_holes(
        start: int, end: int, sections: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        if not sections:
            return [(start, end)]
        sorted_sections = sorted(sections, key=lambda x: x[0])
        res = []

        sec_limit = start

        for s_s, s_e in sorted_sections:
            if sec_limit == s_s:
                # all good
                pass
            elif sec_limit < s_s:
                # missing until start of section
                res.append((sec_limit, s_s))
            else:  # sec_limit > s_s
                logger.error("Logic error")
            sec_limit = s_e

        if sec_limit < end:
            res.append((sec_limit, end))

        return res

    @staticmethod
    def find_intersections(start: int, end: int, b_to_c: T) -> T:
        res: T = {}
        for (from_b, to_b), (from_c, to_c) in b_to_c.items():
            intersection = TaskInput.get_intersection(start, end, from_b, to_b)
            if intersection:
                res[intersection] = (
                    from_c - from_b + intersection[0],
                    to_c - to_b + intersection[1],
                )

        holes = TaskInput.find_holes(start, end, list(res.keys()))
        for (h_s, h_e) in holes:
            res[(h_s, h_e)] = (h_s, h_e)
        return res

    @staticmethod
    def flatten_map(a_to_b: T, b_to_c: T) -> T:
        res: T = {}
        for (from_a, _), (from_b, to_b) in a_to_b.items():
            b_to_c_sections = TaskInput.find_intersections(from_b, to_b, b_to_c)
            for (from_b_section, to_b_section), (
                from_c,
                to_c,
            ) in b_to_c_sections.items():
                res[
                    (from_a - from_b + from_b_section, from_a - from_b + to_b_section)
                ] = (from_c, to_c)
        return res

    def get_seed_to_location_map(self, seed_ranges: T) -> T:
        return TaskInput.flatten_map(
            TaskInput.flatten_map(
                TaskInput.flatten_map(
                    TaskInput.flatten_map(
                        TaskInput.flatten_map(
                            TaskInput.flatten_map(
                                TaskInput.flatten_map(
                                    seed_ranges,
                                    self.seed_to_soil,
                                ),
                                self.soil_to_fertilizer,
                            ),
                            self.fertilizer_to_water,
                        ),
                        self.water_to_light,
                    ),
                    self.light_to_temperature,
                ),
                self.temperature_to_humidity,
            ),
            self.humidity_to_location,
        )

    @staticmethod
    def batched(iterable, n):
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch

    def get_min_location_for_seed_ranges(self) -> int:
        seed_ranges = {
            (seed_s, seed_s + seed_c): (seed_s, seed_s + seed_c)
            for seed_s, seed_c in self.batched(self.seeds, 2)
        }
        seed_to_location_map = self.get_seed_to_location_map(seed_ranges)
        return min(seed_to_location_map.values(), key=lambda x: x[0])[0]

    def map_seed_to_location(self, i: int) -> int:
        seed = self.seeds[i]
        return TaskInput.get_mapped(
            self.humidity_to_location,
            TaskInput.get_mapped(
                self.temperature_to_humidity,
                TaskInput.get_mapped(
                    self.light_to_temperature,
                    TaskInput.get_mapped(
                        self.water_to_light,
                        TaskInput.get_mapped(
                            self.fertilizer_to_water,
                            TaskInput.get_mapped(
                                self.soil_to_fertilizer,
                                TaskInput.get_mapped(self.seed_to_soil, seed),
                            ),
                        ),
                    ),
                ),
            ),
        )

    @staticmethod
    def read(lines: list[str]) -> "TaskInput":
        (
            raw_seeds,
            raw_seed_to_soil,
            raw_soil_to_fertilizer,
            raw_fertilizer_to_water,
            raw_water_to_light,
            raw_light_to_temperature,
            raw_temperature_to_humidity,
            raw_humidity_to_location,
        ) = split_lines_by_empty_line(lines)

        seeds = [int(s) for s in raw_seeds[0].split(":")[1].split()]

        def get_values(ls: list[str]) -> T:
            res = {}
            for line in ls[1:]:
                d_s, s_s, length = [int(s) for s in line.split()]
                res[(s_s, s_s + length)] = (d_s, d_s + length)
            return res

        return TaskInput(
            seeds,
            get_values(raw_seed_to_soil),
            get_values(raw_soil_to_fertilizer),
            get_values(raw_fertilizer_to_water),
            get_values(raw_water_to_light),
            get_values(raw_light_to_temperature),
            get_values(raw_temperature_to_humidity),
            get_values(raw_humidity_to_location),
        )


def get_seed_to_location(task_input: TaskInput) -> dict[int, int]:
    res = {}
    for i, seed in enumerate(task_input.seeds):
        res[seed] = task_input.map_seed_to_location(i)
    return res


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    lines = reader.file_to_lines(5)
    logger.info(f"{lines[:3]=}...")

    task_input = TaskInput.read(lines)

    seed_to_location = get_seed_to_location(task_input)

    res_1 = min(seed_to_location.values())
    logger.info(f"{res_1=}")

    res_2 = task_input.get_min_location_for_seed_ranges()
    logger.info(f"{res_2=}")

    return res_1, res_2
