import logging

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, convert, tokenize

logger = logging.getLogger(__name__)


def get_all_neighbors(cube: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    return {
        (cube[0] - 1, cube[1], cube[2]),
        (cube[0] + 1, cube[1], cube[2]),
        (cube[0], cube[1] - 1, cube[2]),
        (cube[0], cube[1] + 1, cube[2]),
        (cube[0], cube[1], cube[2] - 1),
        (cube[0], cube[1], cube[2] + 1),
    }


def get_neighbours_of(
    cubes: set[tuple[int, int, int]], cube: tuple[int, int, int]
) -> set[tuple[int, int, int]]:
    neighbors = get_all_neighbors(cube)
    return cubes.intersection(neighbors)


def get_neighbours(
    cubes: set[tuple[int, int, int]], with_cubes: set[tuple[int, int, int]]
) -> dict[tuple[int, int, int], set[tuple[int, int, int]]]:
    res: dict[tuple[int, int, int], set[tuple[int, int, int]]] = {}
    for cube in cubes:
        res[cube] = get_neighbours_of(with_cubes, cube)
    return res


def get_frame(cubes: set[tuple[int, int, int]]) -> tuple[int, int, int, int, int, int]:
    return (
        min(c[0] for c in cubes),
        max(c[0] for c in cubes),
        min(c[1] for c in cubes),
        max(c[1] for c in cubes),
        min(c[2] for c in cubes),
        max(c[2] for c in cubes),
    )


def is_in_frame(
    point: tuple[int, int, int],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    z_min: int,
    z_max: int,
) -> bool:
    return all(
        [
            point[0] >= x_min,
            point[0] <= x_max,
            point[1] >= y_min,
            point[1] <= y_max,
            point[2] >= z_min,
            point[2] <= z_max,
        ]
    )


def can_reach_outside_in_dir(
    diff: tuple[int, int, int],
    starting_point: tuple[int, int, int],
    cubes: set[tuple[int, int, int]],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    z_min: int,
    z_max: int,
) -> bool:
    point = starting_point
    while is_in_frame(point, x_min, x_max, y_min, y_max, z_min, z_max):
        point = (
            point[0] + diff[0],
            point[1] + diff[1],
            point[2] + diff[2],
        )
        if point in cubes:
            return False
    return True


def can_reach_outside(
    starting_point: tuple[int, int, int],
    cubes: set[tuple[int, int, int]],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    z_min: int,
    z_max: int,
) -> bool:
    diffs = {
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    }

    return any(
        can_reach_outside_in_dir(
            diff, starting_point, cubes, x_min, x_max, y_min, y_max, z_min, z_max
        )
        for diff in diffs
    )


def build_hole(
    starting_point: tuple[int, int, int],
    cubes: set[tuple[int, int, int]],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    z_min: int,
    z_max: int,
) -> frozenset[tuple[int, int, int]]:
    hole: set[tuple[int, int, int]] = {starting_point}
    queue = {starting_point}
    while queue:
        this = queue.pop()
        hole_candidates = get_all_neighbors(this).difference(cubes).difference(hole)
        if any(
            can_reach_outside(c, cubes, x_min, x_max, y_min, y_max, z_min, z_max)
            for c in hole_candidates
        ):
            return frozenset()
        hole = hole.union(hole_candidates)
        queue = queue.union(hole_candidates)
    return frozenset(hole)


def try_find_hole_from_starting_point(
    starting_point: tuple[int, int, int],
    cubes: set[tuple[int, int, int]],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    z_min: int,
    z_max: int,
) -> frozenset[tuple[int, int, int]]:
    if starting_point in cubes or can_reach_outside(
        starting_point, cubes, x_min, x_max, y_min, y_max, z_min, z_max
    ):
        return frozenset()

    return build_hole(starting_point, cubes, x_min, x_max, y_min, y_max, z_min, z_max)


def get_holes(cubes: set[tuple[int, int, int]]) -> set[frozenset[tuple[int, int, int]]]:
    x_min, x_max, y_min, y_max, z_min, z_max = get_frame(cubes)
    logger.info(f"{x_min=} {x_max=} {y_min=} {y_max=} {z_min=} {z_max=}")
    holes: set[frozenset[tuple[int, int, int]]] = set()

    for x in range(x_min - 1, x_max + 1):
        for y in range(y_min - 1, y_max + 1):
            for z in range(z_min - 1, z_max + 1):
                starting_point = (x, y, z)
                if any(starting_point in hole for hole in holes):
                    continue
                hole = try_find_hole_from_starting_point(
                    starting_point, cubes, x_min, x_max, y_min, y_max, z_min, z_max
                )
                if hole:
                    holes.add(hole)
    return holes


def get_outer_surface(
    neighbours: dict[tuple[int, int, int], set[tuple[int, int, int]]],
    hole: set[tuple[int, int, int]],
) -> dict[tuple[int, int, int], set[tuple[int, int, int]]]:
    outer_surface = {
        cube: get_all_neighbors(cube).difference(this_neighbours).difference(hole)
        for cube, this_neighbours in neighbours.items()
    }
    return outer_surface


test_inp = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    iinp = reader.file_to_lines(18)
    # iinp = test_inp.split("\n")
    inp = convert(tokenize(iinp), int)
    cubes = {(x, y, z) for x, y, z in inp}
    # logger.info(f"{cubes=}")
    neighbours = get_neighbours(cubes, cubes)

    res_1 = 6 * len(cubes) - sum(len(n) for n in neighbours.values())
    logger.info(f"{res_1=}")

    holes = get_holes(cubes)
    logger.info(f"{len(holes)=}")
    all_holes = set().union(*holes)
    surface = get_outer_surface(neighbours, all_holes)
    res_2 = sum(len(n) for n in surface.values())
    logger.info(f"{res_2=}")

    return res_1, res_2
