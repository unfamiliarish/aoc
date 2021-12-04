import __main__

from typing import Sequence, Tuple
from math import prod

from aoc.utils import read_file


def get_new_position(commands: Tuple[str,int]) -> Tuple[int, int]:
    x = y = 0
    for command in commands:
        if command[0] == "forward":
            x += command[1]
        elif command[0] == "up":
            y -= command[1]
        elif command[0] == "down":
            y += command[1]

    return x, y

def get_position_from_aim(commands: Tuple[str,int]) -> Tuple[int,int]:
    x = y = aim = 0
    for command in commands:
        if command[0] == "forward":
            x += command[1]
            y += aim * command[1]
        elif command[0] == "up":
            aim -= command[1]
        elif command[0] == "down":
            aim += command[1]
        
    return x, y


def solution() -> None:
    file_rows = read_file("input", __file__)
    split_commands = [row.split() for row in file_rows]
    commands = [(c[0], int(c[1])) for c in split_commands]

    position_simple = get_new_position(commands)
    position_from_aim = get_position_from_aim(commands)

    print(f"solution 1: {prod(position_simple)}")
    print(f"solution 2: {prod(position_from_aim)}")
