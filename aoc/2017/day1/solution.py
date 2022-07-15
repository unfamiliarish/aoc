from aoc.utils import read_file


def solution(num: int) -> int:
    


num1 = '1122'
num2 = '1111'
num3 = '1234'
num4 = '9121212129'

if not solution(num1) == 3:
    print("1 oh no")
if not solution(num2) == 4:
    print("2 oh no")
if not solution(num3) == 0:
    print("3 oh no")
if not solution(num4) == 1:
    print("4 oh no")


file_num = read_file("input", __file__)[0]
val = solution(file_num)
print(val)
