import utils


def is_nice_string(input: str) -> bool:
    vowel_count = 0
    for v in "aeiou":
        vowel_count += input.count(v)

    has_double_letter = False
    for i, val in enumerate(input[1:]):
        if input[i] == val:
            has_double_letter = True

    contains_invalid_substring = False
    invalid_substrings = ["ab", "cd", "pq", "xy"]
    for string in invalid_substrings:
        if input.find(string) != -1:
            contains_invalid_substring = True

    return vowel_count >= 3 and has_double_letter and not contains_invalid_substring


def count_nice_strings(filename) -> int:
    lines = utils.import_file(filename)

    nice_strings = 0
    for line in lines:
        if is_nice_string(line):
            nice_strings += 1

    return nice_strings


def redo_is_nice_string(input: str) -> bool:
    pass


print("running tests for is_nice_string")
assert is_nice_string("ugknbfddgicrmopn") is True
assert is_nice_string("aaa") is True
assert is_nice_string("jchzalrnumimnmhp") is False
assert is_nice_string("haegwjzuvuyypxyu") is False
assert is_nice_string("dvszwmarrgswjxmb") is False
print("all tests passed")

nice_string_count = count_nice_strings("input")
print(nice_string_count)
