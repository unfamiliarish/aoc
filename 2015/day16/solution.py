import re

import utils


def parse_sue_data(sue_str: str) -> dict:
    sue_data = {}

    split = sue_str.split(": ")
    sue_data["number"] = int(split[0].split(" ")[1])

    properties = []
    for s in split[1:]:
        if ", " in s:
            properties = properties + s.split(", ")
        else:
            properties.append(s)

    for i in range(0, len(properties), 2):
        sue_data[properties[i]] = int(properties[i + 1])

    return sue_data


def sue_matches(sue: dict, sue_info: dict) -> bool:
    for key, val in sue.items():
        if key == "number":
            continue

        if key not in sue_info or sue_info[key] != val:
            return False

    return True


def sue_matches_with_ranges(sue: dict, sue_info: dict) -> bool:
    for key, val in sue.items():
        if key == "number":
            continue

        if key == "cats" or key == "trees":
            if sue_info[key] >= val:
                return False
            return True
        elif key == "pomeranians" or key == "goldfish":
            if sue_info[key] <= val:
                return False
            return True

        if key not in sue_info or sue_info[key] != val:
            return False

    return True


def find_matching_sue_number(
    sue_file: str, sues_file: str, ranges: bool = False
) -> int:
    # sue_file is info describing sue who gave gift
    # sues_file is all possible sues
    sue_info = utils.import_json_file(sue_file)
    sues_raw = utils.import_file(sues_file)
    sues = [parse_sue_data(raw_sue) for raw_sue in sues_raw]

    matching_sue = {}
    for sue in sues:
        if (not ranges and sue_matches(sue, sue_info)) or (
            ranges and sue_matches_with_ranges(sue, sue_info)
        ):
            matching_sue = sue

    return matching_sue["number"]


part_1_result = find_matching_sue_number("sue_info.json", "input")
assert find_matching_sue_number("sue_info.json", "input") == 40
print(f"part 1: {part_1_result}")

# 496 too high
part_2_result = find_matching_sue_number("sue_info.json", "input", ranges=True)
print(f"part 2: {part_2_result}")

sue_info = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

assert (
    sue_matches({'number': 1, 'goldfish': 9, 'cars': 0, 'samoyeds': 9}, sue_info)
) is False

assert (
    sue_matches({'number': 1, 'goldfish': 5, 'cars': 2, 'samoyeds': 2}, sue_info)
) is True

# all match
sue_1 = {
    'children': 3,
    'cats': 10,
    'samoyeds': 2,
    'pomeranians': 0,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 4,
    'trees': 13,
    'cars': 2,
    'perfumes': 1,
}

# none match
sue_2 = {
    'children': 3,
    'cats': 2,
    'samoyeds': 2,
    'pomeranians': 4,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 6,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

keys = ["cats", "trees", "pomeranians", "goldfish"]

for key in keys:
    sue1 = sue_1.copy()
    sue2 = sue_2.copy()

    del sue1[key], sue2[key]
    assert sue_matches_with_ranges(sue1, sue_info) is True
    assert sue_matches_with_ranges(sue2, sue_info) is False
