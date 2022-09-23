import utils


def solution():
    floor_codes = utils.import_file("input")[0]

    floor = 0
    for dir in floor_codes:
        if dir == "(":
            floor += 1
        elif dir == ")":
            floor -= 1
        else:
            raise ValueError("floor code not recognized")

    print(f"solution 1: {floor}")
    return floor


solution()
