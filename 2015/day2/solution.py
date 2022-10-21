from math import prod
import utils


def calc_paper(dimensions: str) -> int:
    sides = [int(side) for side in dimensions.split("x")]

    smallest = float("inf")
    sq_ft = 0
    for l, w in utils.pair_elements(sides):
        area = l * w
        if area < smallest:
            smallest = area

        sq_ft += 2 * area

    return sq_ft + smallest


def calc_all_paper(filename: str) -> int:
    lines = utils.import_file(filename)

    total_paper = 0
    for line in lines:
        total_paper += calc_paper(line)

    return total_paper


def calc_ribbon(dimensions: str) -> int:
    sides = [int(side) for side in dimensions.split("x")]
    sides.sort()

    return prod(sides) + 2 * (sides[0] + sides[1])


def calc_all_ribbon(filename: str) -> int:
    lines = utils.import_file(filename)

    total_ribbon = 0
    for line in lines:
        total_ribbon += calc_ribbon(line)

    return total_ribbon


filename = "input"

all_paper = calc_all_paper(filename)
all_ribbon = calc_all_ribbon(filename)

print(f"total paper: {all_paper}")
print(f"total ribbon: {all_ribbon}")
