import hashlib
import time


def find_5_leading_zeros_number(secret_key: str) -> int:
    hash_num = 0
    while True:
        hash_input = secret_key + str(hash_num)
        hash = hashlib.md5(hash_input.encode())
        hex_hash = hash.hexdigest()
        if hex_hash[:5] == "00000":
            return hash_num

        hash_num += 1


def find_6_leading_zeros_number(secret_key: str) -> int:
    hash_num = 0
    while True:
        hash_input = secret_key + str(hash_num)
        hash = hashlib.md5(hash_input.encode())
        hex_hash = hash.hexdigest()
        if hex_hash[:6] == "000000":
            return hash_num

        hash_num += 1


start = time.time()

assert find_5_leading_zeros_number("abcdef") == 609043
test1 = time.time()
print(f"test1 time: {test1 - start}s")

assert find_5_leading_zeros_number("pqrstuv") == 1048970
test2 = time.time()
print(f"test2 time: {test2 - start}s")

day1_answer = find_5_leading_zeros_number("bgvyzdsv")
day1_time = time.time()
print(f"day1 time: {day1_time - start}")
print(f"day1 answer: {day1_answer}")

day2_answer = find_6_leading_zeros_number("bgvyzdsv")
day2_time = time.time()
print(f"day2 time: {day2_time - start}")
print(f"day2 answer: {day2_answer}")
