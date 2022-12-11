# master utils file
# accums utils over implemented solutions

import json


def import_file(filename: str) -> list:
    with open(filename, "r") as file_pointer:
        lines = file_pointer.readlines()

    return [line.strip() for line in lines]


def import_json_file(filename: str) -> dict:
    with open(filename, "r") as fp:
        data = json.load(fp)

    return data


def pair_elements(list_: list):
    return zip(list_, list_[1:] + list_[:1])
