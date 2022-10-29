from hashlib import new
import utils


def count_in_memory_chars(string: str) -> int:
    characters = string[1:-1]

    char_count = 0
    i = 0
    while i < len(characters):
        char_count += 1
        if characters[i] == "\\":
            if characters[i + 1] == "x":
                i += 3
            else:
                i += 1

        i += 1

    return char_count


def count_new_encoding_chars(string: str) -> int:
    char_count = 0
    for char in string:
        if char == "\\" or char == "\"":
            char_count += 1

        char_count += 1

    return char_count + 2


def count_char_difference(filename: str) -> int:
    strings = utils.import_file(filename)

    char_count_diff = 0
    for string in strings:
        char_count_diff += len(string) - count_in_memory_chars(string)

    return char_count_diff


def count_new_encoding_char_difference(filename: str) -> int:
    strings = utils.import_file(filename)

    encoding_diff_count = 0
    for string in strings:
        new_encoding_literals_count = count_new_encoding_chars(string)
        encoding_diff_count += new_encoding_literals_count - len(string)

    return encoding_diff_count


assert count_in_memory_chars('""') == 0
assert count_in_memory_chars('"abc"') == 3
assert count_in_memory_chars('"aaa\\"aaa"') == 7
assert count_in_memory_chars('"aaa\\\\aaa"') == 7
assert count_in_memory_chars('"\x27"') == 1
assert count_in_memory_chars('"   "') == 3

assert count_new_encoding_chars('""') == 6
assert count_new_encoding_chars('"abc"') == 9
assert count_new_encoding_chars('"aaa\\"aaa"') == 16
assert count_new_encoding_chars('"aaa\\\\aaa"') == 16
assert count_new_encoding_chars('"\\x27"') == 11
assert count_new_encoding_chars('"   "') == 9


assert count_char_difference("input_sm") == 12
assert count_new_encoding_char_difference("input_sm") == 19

char_diff_1 = count_char_difference("input")
print(f"part 1: {char_diff_1}")

char_diff_2 = count_new_encoding_char_difference("input")
print(f"part 2: {char_diff_2}")
