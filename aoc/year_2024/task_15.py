import logging
from dataclasses import dataclass

from aoc.registry import SolutionRegistry
from aoc.util.reader import Reader, split_lines_by_empty_line, tokenize_by_char

logger = logging.getLogger(__name__)


@dataclass(frozen=True, unsafe_hash=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Pos") -> "Pos":
        return Pos(self.x - other.x, self.y - other.y)


MOVEMENTS = {
    "^": Pos(-1, 0),
    ">": Pos(0, 1),
    "<": Pos(0, -1),
    "v": Pos(1, 0),
}


class Warehouse:
    def __init__(self, map: list[list[str]]) -> None:
        self.map = map
        self.pos = self.get_start_pos(self.map)

    def __repr__(self) -> str:
        return "\n" + "\n".join("".join(line) for line in self.map)

    @staticmethod
    def get_start_pos(map: list[list[str]]) -> Pos:
        for x, line in enumerate(map):
            for y, c in enumerate(line):
                if c == "@":
                    return Pos(x, y)
        raise Exception("could not find starting pos")

    def _gps_value(self, start: str) -> int:
        res = 0
        for x, line in enumerate(self.map):
            for y, c in enumerate(line):
                if c == start:
                    res += 100 * x + y
        return res

    def can_move(self, pos: Pos, dir: Pos) -> set[Pos]:
        current = self.map[pos.x][pos.y]
        if current == ".":
            return {pos}
        if current == "#":
            return set()
        if current == "O":
            s1 = self.can_move(pos + dir, dir)
            return s1.union({pos}) if s1 else set()
        if current == "[":
            s1 = self.can_move(pos + dir, dir)
            s2 = set()
            if dir.x:
                s2 = self.can_move(pos + dir + Pos(0, 1), dir)
                if not s2:
                    return set()
            return s1.union(s2).union({pos}) if s1 else set()
        if current == "]":
            s1 = self.can_move(pos + dir, dir)
            s2 = set()
            if dir.x:
                s2 = self.can_move(pos + dir + Pos(0, -1), dir)
                if not s2:
                    return set()
            return s1.union(s2).union({pos}) if s1 else set()
        raise Exception(f"impossibru: {current}")

    def move(self, dir: Pos) -> None:
        current_pos = self.pos
        target_set = self.can_move(current_pos + dir, dir)
        if not target_set:
            return

        from_dir = Pos(-1 * dir.x, -1 * dir.y)
        targets = list(target_set)
        targets.sort(key=lambda p: p.x * from_dir.x + p.y * from_dir.y)

        for p in targets:
            from_p = Pos(p.x + from_dir.x, p.y + from_dir.y)
            orig_v = self.map[from_p.x][from_p.y]
            self.map[p.x][p.y] = orig_v
            if from_p not in target_set:
                self.map[from_p.x][from_p.y] = "."

        self.pos = self.pos + dir


class NarrowWarehouse(Warehouse):
    def __init__(self, raw_map: list[str]) -> None:
        super().__init__(tokenize_by_char(raw_map))

    def gps_value(self):
        return super()._gps_value(start="O")


class WideWarehouse(Warehouse):
    def __init__(self, raw_map: list[str]) -> None:
        super().__init__(tokenize_by_char(self.transform(raw_map)))

    @staticmethod
    def transform(map: list[str]) -> list[str]:
        res: list[str] = []
        for line in map:
            tmp = line.replace("#", "##")
            tmp = tmp.replace("O", "[]")
            tmp = tmp.replace(".", "..")
            tmp = tmp.replace("@", "@.")
            res.append(tmp)
        return res

    def gps_value(self):
        return super()._gps_value(start="[")


@SolutionRegistry.register
def solve(reader: Reader) -> tuple[int, int]:
    raw_map, raw_movements = split_lines_by_empty_line(reader.file_to_lines(15))
    movements: list[Pos] = [MOVEMENTS[m] for line in raw_movements for m in line]

    narrow_warehouse = NarrowWarehouse(raw_map)
    for m in movements:
        narrow_warehouse.move(m)

    res_1 = narrow_warehouse.gps_value()
    logger.info(f"{res_1=}")

    wide_warehouse = WideWarehouse(raw_map)
    for m in movements:
        wide_warehouse.move(m)

    res_2 = wide_warehouse.gps_value()
    logger.info(f"{res_2=}")

    return res_1, res_2
