# master utils file
# accums utils over implemented solutions

from typing import Sequence


def import_file(filename: str) -> Sequence[object]:
    with open(filename, "r") as file_pointer:
        lines = file_pointer.readlines()

    return [line.strip() for line in lines]
