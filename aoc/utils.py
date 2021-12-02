from typing import Sequence

def read_file(filename: str) -> Sequence[str]:
    with open(filename, 'r') as file_stream:
        return [line.strip() for line in file_stream.readlines()]
