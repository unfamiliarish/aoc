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
    strings = utils.import_file(filename)

    nice_strings = 0
    for string in strings:
        if is_nice_string(string):
            nice_strings += 1

    return nice_strings


def redo_is_nice_string(input: str) -> bool:
    double_letters = set()

    curr_letters = input[:2]
    double_letters.add(curr_letters)

    has_double_letter = False
    for i in range(1, len(input)):
        prev_letters = curr_letters
        curr_letters = input[i : i + 2]

        if curr_letters in double_letters:
            if curr_letters != prev_letters:
                has_double_letter = True
                break
            elif (
                curr_letters == prev_letters
                and i > 1
                and curr_letters == input[i - 2 : i]
            ):
                has_double_letter = True
                break

        double_letters.add(curr_letters)

    has_spaced_repeated_letter = False
    for i in range(2, len(input)):
        prev_letter = input[i - 2]
        curr_letter = input[i]
        if prev_letter == curr_letter:
            has_spaced_repeated_letter = True
            break

    return has_double_letter and has_spaced_repeated_letter


def redo_count_nice_strings(filename: str) -> int:
    strings = utils.import_file(filename)

    nice_string_count = 0
    for string in strings:
        if redo_is_nice_string(string):
            nice_string_count += 1

    return nice_string_count


print("running tests for is_nice_string")
assert is_nice_string("ugknbfddgicrmopn") is True
assert is_nice_string("aaa") is True
assert is_nice_string("jchzalrnumimnmhp") is False
assert is_nice_string("haegwjzuvuyypxyu") is False
assert is_nice_string("dvszwmarrgswjxmb") is False
print("all tests passed\n")

nice_string_count = count_nice_strings("input")
print(f"nice string count: {nice_string_count}\n")

print("running tests for redo_is_nice_string")
assert redo_is_nice_string("qjhvhtzxzqqjkmpb") is True
assert redo_is_nice_string("xxyxx") is True
assert redo_is_nice_string("uuuu") is True
assert redo_is_nice_string("uurcxstgmygtbstg") is False
assert redo_is_nice_string("ieodomkazucvgmuy") is False
print("all tests passed\n")

redo_nice_string_count = redo_count_nice_strings("input")
print(f"redo nice string count: {redo_nice_string_count}")
