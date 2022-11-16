from collections import defaultdict
from dataclasses import dataclass, field

import utils


@dataclass
class Seat:
    name: str
    right: "Seat" = None
    left: "Seat" = None

    def __repr__(self) -> str:
        right = f'Seat(name="{self.right.name}")' if self.right else None
        left = f'Seat(name="{self.left.name}")' if self.left else None

        return f'Seat(name="{self.name}", right={right}, left={left})'


@dataclass
class Table:
    first_seat: Seat = None  # type: ignore
    seats: dict = field(default_factory=lambda: defaultdict(Seat))  # type: ignore
    guest_preferences: dict = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )  # type: ignore

    def populate_guest_preferences(self, happiness_prefs: list) -> None:
        for pref in happiness_prefs:
            name = pref[0]
            neighbor = pref[1]
            happiness = pref[2]

            # undirected graph
            self.guest_preferences[name][neighbor] += happiness
            self.guest_preferences[neighbor][name] += happiness

    def seat_new_person(self, name: str) -> None:
        seats = self.seats
        new_seat = Seat(name)

        if len(seats) == 0:
            self.first_seat = new_seat
            new_seat.right = new_seat
            new_seat.left = new_seat
            seats[name] = new_seat

            return

        left_neighbor = self.first_seat
        right_neighbor = left_neighbor.right

        best_weight = float("-inf")
        best_right = None
        best_left = None
        for _ in range(len(seats)):

            left_neighbor_weight = self.guest_preferences[name][left_neighbor.name]
            right_neighbor_weight = self.guest_preferences[name][right_neighbor.name]
            neighbors_weight = self.guest_preferences[left_neighbor.name][
                right_neighbor.name
            ]

            weight_change_with_new_seat = (
                left_neighbor_weight + right_neighbor_weight - neighbors_weight
            )

            if weight_change_with_new_seat > best_weight:
                best_weight = weight_change_with_new_seat
                best_left = left_neighbor
                best_right = right_neighbor

            left_neighbor = right_neighbor
            right_neighbor = right_neighbor.right

        seats[name] = new_seat
        best_left.right = new_seat
        new_seat.left = best_left
        best_right.left = new_seat
        new_seat.right = best_right

        return

    def get_total_happiness(self) -> int:
        curr_seat = self.first_seat
        next_seat = curr_seat.right

        total_happiness = 0
        for _ in range(len(self.seats)):
            total_happiness += self.guest_preferences[curr_seat.name][next_seat.name]
            if len(self.seats) == 2:
                break

            curr_seat = next_seat
            next_seat = curr_seat.right

        return total_happiness


def parse_happiness(input: str) -> tuple[str, str, int]:
    name, remaining = input.split(" would ")
    happiness_str, neighbor = remaining.split(" happiness units by sitting next to ")
    neighbor = neighbor[:-1]  # remove period

    sign, amount = happiness_str.split(" ")
    happiness = int(amount) if sign == "gain" else -int(amount)

    return (name, neighbor, happiness)


def determine_ideal_seating_happiness(filename: str) -> int:
    rows = utils.import_file(filename)
    guest_prefs = [parse_happiness(row) for row in rows]

    table = Table()
    table.populate_guest_preferences(guest_prefs)

    for name in table.guest_preferences.keys():
        table.seat_new_person(name)

    total_happiness = table.get_total_happiness()

    return total_happiness


# assert determine_ideal_seating_happiness("input_sm") == 330

part_1_result = determine_ideal_seating_happiness("input")
print(f"part 1: {part_1_result}")
