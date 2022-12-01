def import_file(filename: str) -> list[str]:
    with open(filename, "r") as fp:
        return fp.readlines()


def calc_num_container_combos(filename: str) -> int:
    raw_data_lines = import_file(filename)
    containers = [int(line) for line in raw_data_lines]

    pass


assert calc_num_container_combos("input_sm") == 4
