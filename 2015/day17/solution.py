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


assert calc_num_container_combos("input_sm", 25) == 4

part_1_result = calc_num_container_combos("input", 150)
print(f"part 1: {part_1_result}")
