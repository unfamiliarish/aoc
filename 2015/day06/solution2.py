from typing import List
import utils


def turn_on_lights(
    x_0: int, x_n: int, y_0: int, y_n: int, lights: List[List[int]]
) -> None:
    for i in range(x_0, x_n + 1):
        for j in range(y_0, y_n + 1):
            lights[i][j] += 1


def turn_off_lights(
    x_0: int, x_n: int, y_0: int, y_n: int, lights: List[List[int]]
) -> None:
    for i in range(x_0, x_n + 1):
        for j in range(y_0, y_n + 1):
            if lights[i][j] > 0:
                lights[i][j] -= 1


def toggle_lights(
    x_0: int, x_n: int, y_0: int, y_n: int, lights: List[List[int]]
) -> None:
    for i in range(x_0, x_n + 1):
        for j in range(y_0, y_n + 1):
            lights[i][j] += 2


def parse_command(command: str) -> tuple:
    command_pieces = command.split(" ")

    start = [int(x) for x in command_pieces[-3].split(",")]
    end = [int(y) for y in command_pieces[-1].split(",")]

    command = command_pieces[0]
    if command == "turn":
        command = command + " " + command_pieces[1]

    return (command, start[0], end[0], start[1], end[1])


def count_brightness(lights: List[List[bool]]) -> int:
    count = 0
    for i in range(1000):
        for j in range(1000):
            count += lights[i][j]

    return count


def put_up_lights(filename: str) -> int:
    commands = utils.import_file(filename)

    lights = [[False for j in range(1000)] for i in range(1000)]
    for command_raw in commands:
        command = parse_command(command_raw)
        if command[0] == "turn on":
            turn_on_lights(command[1], command[2], command[3], command[4], lights)
        elif command[0] == "turn off":
            turn_off_lights(command[1], command[2], command[3], command[4], lights)
        elif command[0] == "toggle":
            toggle_lights(command[1], command[2], command[3], command[4], lights)
        else:
            raise ValueError(f"invalid lights command: {command[0]}")

    return count_brightness(lights)


assert put_up_lights("input_d2_1") == 1
assert put_up_lights("input_d2_2") == 2000000

total_brightness = put_up_lights("input")
print(total_brightness)
