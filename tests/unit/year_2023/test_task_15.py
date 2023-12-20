import pytest

from aoc.year_2023.task_15 import Box, InitSeq, Lens, elf_hash


@pytest.mark.parametrize(
    "input, expected_hash",
    [
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("cm=2", 47),
        ("qp-", 14),
        ("pc=4", 180),
        ("ot=9", 9),
        ("ab=5", 197),
        ("pc-", 48),
        ("pc=6", 214),
        ("ot=7", 231),
    ],
)
def test_elf_hash(input, expected_hash):
    assert elf_hash(input) == expected_hash


def test_boxes():
    init_seq = InitSeq(
        [
            "rn=1",
            "cm-",
            "qp=3",
            "cm=2",
            "qp-",
            "pc=4",
            "ot=9",
            "ab=5",
            "pc-",
            "pc=6",
            "ot=7",
        ]
    )
    assert init_seq.arrange_boxes()[:4] == [
        Box([Lens("rn", 1), Lens("cm", 2)]),
        Box([]),
        Box([]),
        Box([Lens("ot", 7), Lens("ab", 5), Lens("pc", 6)]),
    ]
