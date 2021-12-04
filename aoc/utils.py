from typing import Sequence

import os

def read_file(file: str, calling_file: str = None) -> Sequence[str]:
    """Returns the contents of file as list of strings

    calling_file provides calling context, for building absolute paths
    """
    if calling_file:
        dir_path=os.path.dirname(calling_file)
        filename = f"{dir_path}/{file}"

    with open(filename, 'r') as file_stream: 
        return [line.strip() for line in file_stream.readlines()]
