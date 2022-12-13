from collections import defaultdict
from pprint import pprint

import utils


def build_molecule_map(raw_mapping: list[str]) -> dict[str, list[str]]:
    molecule_map: dict[str, list] = defaultdict(list)
    for raw_map in raw_mapping:
        base, replacement = raw_map.split(" => ")
        molecule_map[base].append(replacement)

    return molecule_map


def build_reverse_molecule_map(raw_mapping: list[str]) -> dict:
    reverse_molecule_map = {}
    for raw_map in raw_mapping:
        base, replacement = raw_map.split(" => ")
        reverse_molecule_map[replacement] = base

    return reverse_molecule_map


def find_all(input: str, substr: str) -> list[int]:
    locations = []

    start = 0
    while True:
        loc = input.find(substr, start)
        if loc == -1:
            break

        locations.append(loc)
        start = loc + len(substr)

    return locations


def split_at_index(input: str, substr: str, index: int) -> list:
    first = input[:index]

    if index + len(substr) == len(input):
        last = ""
    else:
        last = input[index + len(substr) :]

    return [first, last]


def calc_molecule_set_with_replacement(
    molecule: str, substr: str, new_substr: str
) -> set[str]:
    """Given an input molecule string, return distinct set of strings with a
    single replacement of substr with new_substr
    """
    distinct_molecules = set()

    all_indexes = find_all(molecule, substr)
    for index in all_indexes:
        a, b = split_at_index(molecule, substr, index)
        new_molecule = a + new_substr + b
        distinct_molecules.add(new_molecule)

    return distinct_molecules


def calc_set_of_distinct_molecules(molecule: str, molecule_map: dict) -> set:
    distinct_molecules = set()
    for atom in molecule_map.keys():
        for new_atom in molecule_map[atom]:
            new_molecules = calc_molecule_set_with_replacement(molecule, atom, new_atom)
            distinct_molecules.update(new_molecules)

    return distinct_molecules


def get_num_distinct_molecules(filename: str) -> int:
    raw_input = utils.import_file(filename)

    molecule = raw_input[-1]
    molecule_map = build_molecule_map(raw_input[:-2])

    distinct_molecules = calc_set_of_distinct_molecules(molecule, molecule_map)

    return len(distinct_molecules)


# data structures:
# - molecule -> depth
# - depth -> all poss molecules

# if molecule already exists in first strucutre, do not add it to new depth


# start structures with
# {"e": 0} <- not defaultdict
# {0: ["e"]} <- defaultdict(list), so that at depth we can just append

# i don't want to do depth-first
# i want to do breadth-first

# for all molecules at current depth, calculate the new molecules with the molecule map
# and store them accordingly


def filter_invalid_molecules(molecules: set[str], base_molecule: str) -> set[str]:
    valid_molecules = set()
    for molecule in molecules:
        if molecule.find(base_molecule) >= 0:
            if len(molecule) != len(base_molecule):
                continue

        valid_molecules.add(molecule)

    return valid_molecules


def steps_to_make_medicine(
    goal_molecule: str, base_molecule: str, molecule_map: dict[str, list[str]]
) -> int:
    """example dictionaries below for illustration,
    not accuracy between each other

    molecule_shortest_depth = {
        "a":2,
        "b":12,
        "c":5,
        etc
    }
    molecules_at_depth = {
        0: ["e"],
        1: ["a","b"],
        2: ["c","d","e","f"],
        etc
    }
    """

    molecules_at_step = defaultdict(list)

    molecule_fewest_steps = {goal_molecule: 0}
    molecules_at_step[0].append(goal_molecule)

    curr_depth = 0
    while base_molecule not in molecule_fewest_steps:
        print(curr_depth)
        pprint(len(molecules_at_step[curr_depth]))
        molecules_at_curr_step = molecules_at_step[curr_depth]
        # breakpoint()
        for molecule in molecules_at_curr_step:
            next_depth = curr_depth + 1
            next_depth_molecules = calc_set_of_distinct_molecules(
                molecule, molecule_map
            )
            filtered_molecules = filter_invalid_molecules(
                next_depth_molecules, base_molecule
            )

            for next_molecule in filtered_molecules:
                # breakpoint()
                if next_molecule == base_molecule:
                    return curr_depth + 1
                if next_molecule not in molecule_fewest_steps:
                    molecule_fewest_steps[next_molecule] = next_depth
                    molecules_at_step[next_depth].append(next_molecule)

        curr_depth += 1

    # didn't work
    return -1


def steps_to_make_medicine_in_file(filename: str) -> int:
    raw_data = utils.import_file(filename)
    molecule = raw_data[-1]
    # molecule_map = build_molecule_map(raw_data[:-2])
    reverse_molecule_map = build_reverse_molecule_map(raw_data[:-2])

    return steps_to_make_medicine(molecule, "e", reverse_molecule_map)


# sm_input = utils.import_file("input1_sm")
# assert build_molecule_map(sm_input[:-2]) == {
#     "H": ["HO", "OH"],
#     "O": ["HH"],
#     "F": ["HH"],
# }

# assert find_all("abdbfbdhh", "bd") == [1, 5]
# assert find_all("abdbfbdhh", "w") == []

# assert get_num_distinct_molecules("input1_sm") == 4
# assert get_num_distinct_molecules("input1_sm2") == 7

# part_1_result = get_num_distinct_molecules("input")
# print(f"part 1: {part_1_result}")


assert steps_to_make_medicine_in_file("input2_sm") == 3
assert steps_to_make_medicine_in_file("input2_sm2") == 6

part_2_result = steps_to_make_medicine_in_file("input")
print(f"part 2: {part_2_result}")
