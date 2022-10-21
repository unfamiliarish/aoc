from collections import defaultdict
import utils


def calc_santa_houses(filename):
    directions = utils.import_file(filename)[0]

    location = [0, 0]  # x,y location
    houses = defaultdict(set)
    houses[location[0]].add(location[1])

    for dir in directions:
        if dir == ">":
            location[0] += 1
        elif dir == "<":
            location[0] -= 1
        elif dir == "^":
            location[1] += 1
        elif dir == "v":
            location[1] -= 1
        else:
            raise ValueError("invalid direction value")

        houses[location[0]].add(location[1])

    num_houses = 0
    for x in houses.keys():
        num_houses += len(houses[x])

    return num_houses


def get_updated_location(dir: str):
    if dir == ">":
        return ("x", 1)
    elif dir == "<":
        return ("x", -1)
    elif dir == "^":
        return ("y", 1)
    elif dir == "v":
        return ("y", -1)
    else:
        raise ValueError("invalid direction value")


def calc_robo_santa_houses(filename: str) -> int:
    directions = utils.import_file(filename)[0]

    santa_loc = [0, 0]  # x,y location
    robo_loc = [0, 0]
    houses = defaultdict(set)
    houses[santa_loc[0]].add(santa_loc[1])
    houses[robo_loc[0]].add(robo_loc[1])

    is_santa = True
    for dir in directions:
        coord, shift = get_updated_location(dir)

        if is_santa:
            if coord == "x":
                santa_loc[0] += shift
            elif coord == "y":
                santa_loc[1] += shift

            houses[santa_loc[0]].add(santa_loc[1])
        else:
            if coord == "x":
                robo_loc[0] += shift
            elif coord == "y":
                robo_loc[1] += shift
            houses[robo_loc[0]].add(robo_loc[1])

        is_santa = not is_santa

    num_houses = 0
    for x in houses.keys():
        num_houses += len(houses[x])

    return num_houses


filename = "input"

santa_houses = calc_santa_houses(filename)
robo_santa_houses = calc_robo_santa_houses(filename)

print(f"total santa houses: {santa_houses}")
print(f"total robo houses: {robo_santa_houses}")
