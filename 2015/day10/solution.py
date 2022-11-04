import utils


def look_and_say(input: str) -> str:
    pass


def find_look_and_say_length(look_and_say_str: str, iterations: int) -> int:
    for _ in range(iterations):
        look_and_say_str = look_and_say(look_and_say_str)

    return len(look_and_say_str)


assert look_and_say("1") == "11"
assert look_and_say("11") == "21"
assert look_and_say("21") == "1211"
assert look_and_say("1211") == "111221"
assert look_and_say("111221") == "312211"

part_1_result = find_look_and_say_length("1113222113", 40)
print(f"part 1: {part_1_result}")
