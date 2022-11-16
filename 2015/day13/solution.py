from collections import defaultdict

import utils


def parse_row_to_happiness(row: str) -> tuple[str, str, int]:
    name, remaining = row.split(" would ")
    happiness_details, neighbor = remaining.split(
        " happiness units by sitting next to "
    )
    happiness_sign, happiness_amount = happiness_details.split(" ")

    happiness = (
        int(happiness_amount) if happiness_sign == "gain" else -int(happiness_amount)
    )

    return (name, neighbor[:-1], happiness)


def build_undirected_happiness_graph(happiness_weights: list) -> dict:
    happiness_graph: dict = defaultdict(lambda: defaultdict(int))

    for weight in happiness_weights:
        name = weight[0]
        neighbor = weight[1]
        happiness = weight[2]

        happiness_graph[name][neighbor] += happiness
        happiness_graph[neighbor][name] += happiness

    return happiness_graph


def recurse_find_max_happiness(
    current: str, remaining_to_seat: set, first: str, happiness_graph: dict
) -> int:
    if len(remaining_to_seat) == 0:
        return happiness_graph[current][first]

    weights = []
    for person in remaining_to_seat:
        current_weight = happiness_graph[current][person]
        val = recurse_find_max_happiness(
            person, remaining_to_seat - {person}, first, happiness_graph
        )
        weights.append(current_weight + val)

    return max(weights)


def find_max_happiness(filename: str) -> int:
    rows = utils.import_file(filename)
    happiness_weights = [parse_row_to_happiness(r) for r in rows]

    happiness_graph = build_undirected_happiness_graph(happiness_weights)
    people_to_seat = set(happiness_graph.keys())
    first_seated = people_to_seat.pop()

    return recurse_find_max_happiness(
        first_seated, people_to_seat, first_seated, happiness_graph
    )


assert parse_row_to_happiness(
    "Alice would gain 54 happiness units by sitting next to Bob."
) == ("Alice", "Bob", 54)
assert find_max_happiness("input_sm") == 330

part_1_result = find_max_happiness("input")
print(f"part 1: {part_1_result}")
