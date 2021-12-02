import __main__
import os

from typing import Sequence

from aoc.utils import read_file

def get_count_increase(depths: Sequence[int]) -> int:
    """Returns the count of depth increase measurements"""
    count = 0
    for i in range(len(depths)-1):
        if depths[i] < depths[i+1]:
            count += 1
    
    return count


def get_count_window_increase(depths: Sequence[int]) -> int:
    """Returns the count of depth three-measurement sliding window increases"""
    count = 0
    for i in range(len(depths)-3):
        sum1 = sum(depths[i:i+3])
        sum2 = sum(depths[i+1:i+4])
        if sum1 < sum2:
            count += 1

    return count


breakpoint()

file_data = read_file("aoc/day1/input")
data = [int(value) for value in file_data]

print(f"solution 1: {get_count_increase(data)}")
print(f"solution 2: {get_count_window_increase(data)}")
