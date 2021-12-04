from typing import Sequence, Tuple, Dict

from copy import copy

from aoc.utils import read_file


def binary_to_int(binary_num: str) -> int:
    num = 0
    for i, bit in enumerate(binary_num[::-1]):
        num += 2**i * int(bit)

    return num


def get_bit_counts(binary_nums: Sequence[str]) -> Sequence[Dict[str,int]]:
    # create array for bit counts
    bit_counts = [{"0": 0, "1": 0} for _ in binary_nums[0]]

    # loop through binary numbers and count bits
    for bnum in binary_nums:
        for i, bit in enumerate(bnum):
            bit_counts[i][bit] += 1
    
    return bit_counts


def get_max_bits(bit_counts: Sequence[Dict[str,int]]) -> Sequence[int]:
    max_bits = [None] * len(bit_counts)
    for i, count in enumerate(bit_counts):
        if count["0"] <= count["1"]:
            max_bits[i] = "1"
        else:
            max_bits[i] = "0"

    return max_bits


def get_gamma_and_epsilon(binary_nums: Sequence[str]) -> Tuple[int, int]:
    """Takes in list of binary numbers and finds int values for rates
    
    Rates gamma and epsilon are first found in binary, then converted to ints
    """
    bit_counts = get_bit_counts(binary_nums)

    # find binary gamma, epsilon
    gamma = epsilon = ""
    for count in bit_counts:
        if count["0"] > count["1"]:
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"

    return binary_to_int(gamma), binary_to_int(epsilon)


def get_power_consumption(gamma: int, epsilon: int) -> int:
    return gamma * epsilon



def filter_oxygen(binary_nums: Sequence[str], loc: int) -> str:
    if len(binary_nums) == 1:
        return binary_nums[0]

    bit_counts = get_bit_counts(binary_nums)
    max_bits = get_max_bits(bit_counts)

    filtered_oxygen = [
        bnum for bnum in binary_nums if bnum[loc] == max_bits[loc]
    ]
    return filter_oxygen(filtered_oxygen, loc+1)


def filter_co2(binary_nums: Sequence[str], loc: int) -> str:
    if len(binary_nums) == 1:
        return binary_nums[0]

    bit_counts = get_bit_counts(binary_nums)
    max_bits = get_max_bits(bit_counts)

    filtered_co2 = [
        bnum for bnum in binary_nums if bnum[loc] != max_bits[loc]
    ]
    return filter_co2(filtered_co2, loc+1)


def get_oxygen_and_co2(binary_nums: Sequence[str]) -> Tuple[int, int]:    
    filtered_oxygen = filter_oxygen(copy(binary_nums),0)
    filtered_co2 = filter_co2(copy(binary_nums),0)

    oxygen_rating = binary_to_int(filtered_oxygen)
    co2_rating = binary_to_int(filtered_co2)
    return oxygen_rating, co2_rating


def get_life_support_rating(o: int, co2: int) -> int:
    return o * co2


def solution() -> None:
    rows = read_file("input", __file__)
    gamma, epsilon = get_gamma_and_epsilon(rows)
    oxygen_rating, co2_rating = get_oxygen_and_co2(rows)


    print(f"solution 1: {get_power_consumption(gamma, epsilon)}")
    print(f"solution 2: {get_life_support_rating(oxygen_rating, co2_rating)}")
