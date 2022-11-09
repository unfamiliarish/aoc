from collections import defaultdict

import utils


def build_name_to_atom_dict(rows: list[str]) -> dict:
    name_to_atom_dict: dict = defaultdict(str)
    for row in rows:
        atom_info = row.split(",")
        name_to_atom_dict[atom_info[0]] = atom_info[1]

    return name_to_atom_dict


def build_atom_decay_dict(rows: list[str]) -> dict:
    atom_decay_dict: dict = defaultdict(list[str])
    for row in rows:
        atom_info = row.split(",")
        decay_list = [decay_name for decay_name in atom_info[2].split(".")]

        atom_decay_dict[atom_info[1]] = decay_list

    return atom_decay_dict


def get_decayed_atom_length(
    atom_name: str, name_to_atom: dict, atom_decay: dict, count: int
) -> int:
    atom_seq = name_to_atom[atom_name]
    if count == 0:
        return len(name_to_atom[atom_name])

    total = 0
    for atom in atom_decay[atom_seq]:
        length = get_decayed_atom_length(atom, name_to_atom, atom_decay, count - 1)
        total += length

    return total


def get_decayed_length_after_iterations(
    atom_seq: str, filename: str, iterations: int
) -> int:
    rows = utils.import_file(filename)
    name_to_atom = build_name_to_atom_dict(rows)
    atom_decay = build_atom_decay_dict(rows)

    atom_name = [
        atom_name for atom_name, seq in name_to_atom.items() if atom_seq == seq
    ][0]

    return get_decayed_atom_length(atom_name, name_to_atom, atom_decay, iterations)


rows = utils.import_file("input_sm")

assert build_name_to_atom_dict(rows) == {
    "A": "123",
    "B": "1",
    "C": "223",
    "D": "1222331",
    "E": "11",
}
assert build_atom_decay_dict(rows) == {
    "123": ["A"],
    "1": ["A", "A"],
    "223": ["A", "B"],
    "1222331": ["C", "C"],
    "11": ["D", "D"],
}

name_to_atom = build_name_to_atom_dict(rows)
atom_decay = build_atom_decay_dict(rows)
assert get_decayed_atom_length("D", name_to_atom, atom_decay, 4) == 18
assert get_decayed_length_after_iterations("1222331", "input_sm", 4) == 18
assert get_decayed_length_after_iterations("1113222113", "input", 4) == 22

part_2_result = get_decayed_length_after_iterations("1113222113", "input", 50)
print(f"part 2 result: {part_2_result}")
