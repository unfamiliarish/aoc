from collections import namedtuple
from math import floor

import utils


ReindeerFlightInfo = namedtuple(
    "ReindeerFlightInfo", ["name", "acceleration", "endurance_time", "rest_time"]
)


def parse_input_to_reindeer(input: str) -> ReindeerFlightInfo:
    name, remainder = input.split(" can fly ")
    acceleration, remainder = remainder.split(" km/s for ")
    endurance, rest_time = remainder.split(" seconds, but then must rest for ")

    return ReindeerFlightInfo(
        name, int(acceleration), int(endurance), int(rest_time[:-9])
    )


def calc_race_distance(reindeer: ReindeerFlightInfo, race_time: int) -> int:
    # returns the amount of distance reindeer has flown during the race

    full_cycle_time = reindeer.endurance_time + reindeer.rest_time
    num_cycles = floor(race_time / full_cycle_time)

    remaining_race_time = race_time % full_cycle_time
    remaining_flight_time = (
        remaining_race_time
        if remaining_race_time < reindeer.endurance_time
        else reindeer.endurance_time
    )

    return reindeer.acceleration * (
        (num_cycles * reindeer.endurance_time) + remaining_flight_time
    )


def find_winning_reindeer_distance(filename: str, num_seconds: int) -> int:
    rows = utils.import_file(filename)
    reindeers = [parse_input_to_reindeer(r) for r in rows]

    return max(calc_race_distance(r, num_seconds) for r in reindeers)


assert parse_input_to_reindeer(
    "Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds."
) == ReindeerFlightInfo("Vixen", 19, 7, 124)
assert find_winning_reindeer_distance("input_sm", 1000) == 1120

part_1_result = find_winning_reindeer_distance("input", 2503)
print(f"part 1: {part_1_result}")
