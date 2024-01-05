from aoc.year_2023.task_21 import Garden, build_garden_graph, count_reachable_in

INPUT = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".split()


def test_task_21():
    garden = Garden(INPUT)
    garden_graph = build_garden_graph(garden)
    assert count_reachable_in(2, garden.start_pos, garden_graph) == 4
    assert count_reachable_in(6, garden.start_pos, garden_graph) == 16
