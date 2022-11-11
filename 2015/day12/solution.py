import json

from typing import Union


def import_file(filename: str) -> list[str]:
    with open(filename, "r") as fp:
        lines = fp.readlines()

    return [line.strip() for line in lines]


def recurse_js_for_numbers(object_: Union[str, int, list, dict]) -> int:
    object_type = type(object_)
    if object_type == str:
        return 0
    elif object_type == int:
        return object_  # type: ignore
    elif object_type == dict:
        return sum([recurse_js_for_numbers(val) for val in object_.values()])  # type: ignore
    elif object_type == list:
        return sum([recurse_js_for_numbers(val) for val in object_])  # type: ignore
    else:
        raise TypeError("Input as invalid type: {object_type}")


def recurse_js_for_numbers_excl_red(object_: Union[str, int, list, dict]) -> int:
    object_type = type(object_)
    if object_type == str:
        return 0
    elif object_type == int:
        return object_  # type: ignore
    elif object_type == dict:
        if "red" in object_.keys() or "red" in object_.values():  # type: ignore
            return 0
        return sum([recurse_js_for_numbers_excl_red(val) for val in object_.values()])  # type: ignore
    elif object_type == list:
        return sum([recurse_js_for_numbers_excl_red(val) for val in object_])  # type: ignore
    else:
        raise TypeError("Input as invalid type: {object_type}")


def parse_js_for_numbers(filename) -> int:
    rows = import_file(filename)
    json_rows = [json.loads(row) for row in rows]

    return sum([recurse_js_for_numbers(row) for row in json_rows])


def parse_js_for_numbers_excl_red(filename):
    rows = import_file(filename)
    json_rows = [json.loads(row) for row in rows]

    return sum([recurse_js_for_numbers_excl_red(row) for row in json_rows])


part_1_result = parse_js_for_numbers("input")
print(f"part 1: {part_1_result}")

part_2_result = parse_js_for_numbers_excl_red("input")
print(f"part 2: {part_2_result}")
