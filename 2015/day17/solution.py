from collections import defaultdict


def import_file(filename: str) -> list[str]:
    with open(filename, "r") as fp:
        return fp.readlines()


def recurse_count_combos(
    remaining_containers: list[int], num_liters: int, curr_stored: int = 0
) -> int:
    if curr_stored == num_liters:
        return 1

    sized_containers = [
        v for v in remaining_containers if v + curr_stored <= num_liters
    ]  # too long

    total = 0
    while sized_containers:
        size = sized_containers.pop(0)
        result = recurse_count_combos(
            sized_containers, num_liters, curr_stored + size
        )  # too long

        total += result

    return total


def calc_num_container_combos(filename: str, num_liters: int) -> int:
    raw_data_lines = import_file(filename)
    sizes = [int(line) for line in raw_data_lines]
    sized_containers = sorted(sizes, reverse=True)

    return recurse_count_combos(sized_containers, num_liters)


def combine_dicts(dict1: dict, dict2: dict) -> dict:
    new_dict: dict[int, list[int]] = defaultdict(list)
    for key, value in dict1.items():  # value is a list of container sizes
        new_dict[key] = new_dict[key] + value
    for key, value in dict2.items():
        new_dict[key] = new_dict[key] + value

    return new_dict


def recurse_get_combo_containers(
    remaining_containers: list[int],
    goal_liters: int,
    filled_containers: list[int] = [],
) -> dict[int, list[list[int]]]:
    filled_containers = filled_containers.copy()
    if sum(filled_containers) == goal_liters:
        return {len(filled_containers): [filled_containers]}

    containers = [
        c for c in remaining_containers if c + sum(filled_containers) <= goal_liters
    ]

    all_keyed_containers: dict[int, list[list[int]]] = {}
    while containers:
        container = containers.pop()
        keyed_containers = recurse_get_combo_containers(
            containers, goal_liters, filled_containers + [container]
        )

        all_keyed_containers = combine_dicts(all_keyed_containers, keyed_containers)  # type: ignore

    return all_keyed_containers


def get_min_num_container_combos(containers: list[int], goal_liters: int) -> int:
    all_keyed_containers = recurse_get_combo_containers(containers, goal_liters)
    container_sizes = sorted(all_keyed_containers.keys())
    smallest_size = container_sizes[0]

    return len(all_keyed_containers[smallest_size])


def calc_num_min_container_combos(filename: str, goal_liters: int) -> int:
    raw_data_lines = import_file(filename)
    containers = [int(line) for line in raw_data_lines]
    containers.sort()

    return get_min_num_container_combos(containers, goal_liters)


assert calc_num_container_combos("input_sm", 25) == 4

part_1_result = calc_num_container_combos("input", 150)
print(f"part 1: {part_1_result}")

assert calc_num_min_container_combos("input_sm", 25) == 3

part_2_result = calc_num_min_container_combos("input", 150)
print(f"part 2: {part_2_result}")
