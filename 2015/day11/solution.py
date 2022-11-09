import utils


def incr_password(password: str) -> str:
    pass


def pass_includes_3straight(password: str) -> bool:
    pass


def pass_includes_invalid_chars(password: str, invalid_chars: list[str]) -> bool:
    pass


def pass_includes_2_nonoverlapping_pairs(password: str) -> bool:
    pass


def get_next_password(password: str) -> str:
    pass


assert pass_includes_3straight("hijklmmn") == True
assert pass_includes_invalid_chars("hijklmmn", ["i", "o", "l"]) == True
assert pass_includes_2_nonoverlapping_pairs("abbceffg") == True
assert pass_includes_3straight("abbceffg") == True
assert pass_includes_2_nonoverlapping_pairs("abbcegjk") == False

assert get_next_password("abcdefgh") == "abcdffaa"
assert get_next_password("ghijklmn") == "ghjaabcc"
