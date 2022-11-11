import re


def incr_password(password: str) -> str:
    new_pass = ""

    for i, char in enumerate(password[::-1]):
        looped = False
        incr_char = chr(ord(char) + 1)
        if incr_char == "{":
            incr_char = "a"
            looped = True
        new_pass = incr_char + new_pass
        if not looped:
            new_pass = password[: -(i + 1)] + new_pass
            break

    return new_pass


def pass_includes_3straight(password: str) -> bool:
    straight = password[0]
    s_idx = 0

    for char in password[1:]:
        if char == chr(ord(straight[s_idx]) + 1):
            straight += char
            s_idx += 1
        else:
            straight = char
            s_idx = 0

        if s_idx == 2:
            return True

    return False


def pass_includes_invalid_chars(password: str, invalid_chars: list[str]) -> bool:
    return any(char in password for char in invalid_chars)


def pass_includes_2_nonoverlapping_pairs(password: str) -> bool:
    count = 0
    i = 1
    while i < len(password):
        if password[i] == password[i - 1]:
            count += 1
            i += 1

        if count == 2:
            return True

        i += 1

    return False


def get_next_password(password: str) -> str:
    while True:
        password = incr_password(password)
        if pass_includes_invalid_chars(password, ["i", "o", "l"]):
            match = re.search(r"[iol]+", password)
            if match:
                # aaaiobbb - > aaajaaaa
                # len = 8, match.start() = 3 -> 8-1-3 = 4 a's to append
                num_a = len(password) - 1 - match.start()
                incr_letter = chr(ord(match.group()) + 1)  # i->j, l->m, etc
                incr_part = incr_letter + "a" * num_a
                password = password[: match.start()] + incr_part
        if not pass_includes_3straight(password):
            continue
        elif not pass_includes_2_nonoverlapping_pairs(password):
            continue
        break

    return password


assert incr_password("xx") == "xy"
assert incr_password("xz") == "ya"
assert incr_password("abczzz") == "abdaaa"

assert pass_includes_3straight("hijklmmn") is True
assert pass_includes_3straight("abbceffg") is False

assert pass_includes_invalid_chars("hijklmmn", ["i", "o", "l"]) is True
assert pass_includes_invalid_chars("mmmommmm", ["i", "o", "l"]) is True
assert pass_includes_invalid_chars("hijklmmn", ["a", "b"]) is False

assert pass_includes_2_nonoverlapping_pairs("abbceffg") is True
assert pass_includes_2_nonoverlapping_pairs("aaa") is False
assert pass_includes_2_nonoverlapping_pairs("abbcegjk") is False

assert get_next_password("abcdfeaz") == "abcdffaa"
assert get_next_password("abcdefgh") == "abcdffaa"
assert get_next_password("ghijklmn") == "ghjaabcc"


part_1_result = get_next_password("cqjxjnds")
print(f"part 1: {part_1_result}")

part_2_result = get_next_password(part_1_result)
print(f"part 2: {part_2_result}")
