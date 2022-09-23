import utils


def solution1():
    floor_codes = utils.import_file("input")[0]

    floor = 0
    # direction
    for dir in floor_codes:
        if dir == "(":
            floor += 1
        elif dir == ")":
            floor -= 1
        else:
            raise ValueError("floor code not recognized")

    print(f"solution 1: {floor}")


def solution2():
    floor_codes = utils.import_file("input")[0]

    floor = 0
    for i, dir in enumerate(floor_codes):
        if dir == "(":
            floor += 1
        elif dir == ")":
            floor -= 1
        else:
            raise ValueError("floor code not recognized")

        if floor == -1:
            floor_num = i + 1
            break

    print(f"solution 2: {floor_num}")


solution1()
solution2()
