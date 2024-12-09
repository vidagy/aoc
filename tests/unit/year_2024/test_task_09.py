from re import L

from aoc.year_2024.task_09 import Drive, File, Space, merge_spaces

INP = """2333133121414131402"""


def test_task_09_defrag():
    drive = Drive.create([int(i) for i in INP])

    assert drive.defrag().disk == [
        File(length=2, file_id=0),
        File(length=2, file_id=9),
        File(length=1, file_id=8),
        File(length=3, file_id=1),
        File(length=3, file_id=8),
        File(length=1, file_id=2),
        File(length=3, file_id=7),
        File(length=3, file_id=3),
        File(length=1, file_id=6),
        File(length=2, file_id=4),
        File(length=1, file_id=6),
        File(length=4, file_id=5),
        File(length=1, file_id=6),
        File(length=1, file_id=6),
    ]


def test_merge():
    merge_spaces([Space(length=1), Space(length=2)]) == [Space(length=3)]
    merge_spaces([Space(length=1), Space(length=2), Space(length=3)]) == [
        Space(length=6)
    ]
    merge_spaces([Space(length=1), File(length=2, file_id=0), Space(length=3)]) == [
        Space(length=1),
        File(length=2, file_id=0),
        Space(length=3),
    ]
    merge_spaces(
        [
            Space(length=1),
            Space(length=1),
            File(length=2, file_id=0),
            Space(length=1),
            Space(length=3),
        ]
    ) == [Space(length=2), File(length=2, file_id=0), Space(length=4)]
    merge_spaces(
        [
            File(length=2, file_id=0),
            File(length=2, file_id=9),
            Space(length=1),
            File(length=3, file_id=1),
            Space(length=3),
            File(length=1, file_id=2),
            Space(length=3),
            File(length=3, file_id=3),
            Space(length=1),
            File(length=2, file_id=4),
            Space(length=1),
            File(length=4, file_id=5),
            Space(length=1),
            File(length=4, file_id=6),
            Space(length=1),
            File(length=3, file_id=7),
            Space(length=1),
            File(length=4, file_id=8),
            Space(length=0),
        ]
    ) == [
        File(length=2, file_id=0),
        File(length=2, file_id=9),
        Space(length=1),
        File(length=3, file_id=1),
        Space(length=3),
        File(length=1, file_id=2),
        Space(length=3),
        File(length=3, file_id=3),
        Space(length=1),
        File(length=2, file_id=4),
        Space(length=1),
        File(length=4, file_id=5),
        Space(length=1),
        File(length=4, file_id=6),
        Space(length=1),
        File(length=3, file_id=7),
        Space(length=1),
        File(length=4, file_id=8),
        Space(length=0),
    ]


def test_task_09_move():
    drive = Drive.create([int(i) for i in INP])

    assert drive.move_files_left().disk == [
        File(length=2, file_id=0),
        File(length=2, file_id=9),
        File(length=1, file_id=2),
        File(length=3, file_id=1),
        File(length=3, file_id=7),
        Space(length=1),
        File(length=2, file_id=4),
        Space(length=1),
        File(length=3, file_id=3),
        Space(length=4),
        File(length=4, file_id=5),
        Space(length=1),
        File(length=4, file_id=6),
        Space(length=5),
        File(length=4, file_id=8),
        Space(length=2),
    ]
