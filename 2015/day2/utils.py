# master utils file
# accums utils over implemented solutions


def import_file(filename: str) -> list:
    with open(filename, "r") as file_pointer:
        lines = file_pointer.readlines()

    return [line.strip() for line in lines]


def pair_elements(list_: list) -> list:
    return zip(list_, list_[1:] + list_[:1])
