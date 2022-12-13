from collections import defaultdict

import utils


def build_molecule_map(raw_mapping: list[str]) -> dict[str, list[str]]:
    molecule_map: dict[str, list] = defaultdict(list)
    for raw_map in raw_mapping:
        base, replacement = raw_map.split(" => ")
        molecule_map[base].append(replacement)

    return molecule_map


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


sm_input = utils.import_file("input_sm")
assert build_molecule_map(sm_input[:-2]) == {
    "H": ["HO", "OH"],
    "O": ["HH"],
}

assert find_all("abdbfbdhh", "bd") == [1, 5]
assert find_all("abdbfbdhh", "w") == []

assert get_num_distinct_molecules("input_sm") == 4
assert get_num_distinct_molecules("input_sm2") == 7

part_1_result = get_num_distinct_molecules("input")
print(f"part 1: {part_1_result}")
