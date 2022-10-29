from typing import Callable

import utils

# operations
ops: dict[str, Callable] = {
    "ASSIGN": lambda x: x,
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "NOT": lambda a: ~a & 0xFFFF,
    "LSHIFT": lambda a, b: a << b,
    "RSHIFT": lambda a, b: a >> b,
}


def make_ints(strings: list[str]) -> list:
    return [int(s) if s.isnumeric() else s for s in strings]


def parse_instruction(inst: str) -> tuple:
    inst_parts = inst.split(" ")
    inst_parts.remove("->")

    assigned = inst_parts.pop(-1)
    if len(inst_parts) == 3:
        inst = inst_parts.pop(1)
        return (inst, *make_ints(inst_parts), assigned)
    elif len(inst_parts) == 2:
        return (*make_ints(inst_parts), assigned)
    elif len(inst_parts) == 1:
        return ("ASSIGN", *make_ints(inst_parts), assigned)
    else:
        raise ValueError(f"Instruction invalid: {inst}")


def connect_wires(instructions: list[str]) -> dict[str, int]:
    wires: dict[str, int] = {}
    while instructions:
        inst = instructions.pop(0)
        parts = parse_instruction(inst)

        try:
            op = parts[0]
            register = parts[-1]
            input = list(parts[1:-1])

            for i, val in enumerate(input):
                if type(val) is str:
                    input[i] = wires[val]

            wires[register] = ops[op](*input) & 0xFFFF

        except Exception:
            instructions.append(inst)

    return wires


def assemble_circuit(filename) -> int:
    instructions = utils.import_file(filename)
    circuit = connect_wires(instructions)

    return circuit["a"]


assert ops["ASSIGN"](5) == 5
assert ops["AND"](123, 456) == 72
assert ops["OR"](123, 456) == 507
assert ops["LSHIFT"](123, 2) == 492
assert ops["RSHIFT"](456, 2) == 114
assert ops["NOT"](123) == 65412
assert ops["NOT"](456) == 65079


assert parse_instruction("123 -> x") == ("ASSIGN", 123, "x")
assert parse_instruction("456 -> y") == ("ASSIGN", 456, "y")
assert parse_instruction("x AND y -> d") == ("AND", "x", "y", "d")
assert parse_instruction("x OR y -> e") == ("OR", "x", "y", "e")
assert parse_instruction("x LSHIFT 2 -> f") == ("LSHIFT", "x", 2, "f")
assert parse_instruction("y RSHIFT 2 -> g") == ("RSHIFT", "y", 2, "g")
assert parse_instruction("NOT x -> h") == ("NOT", "x", "h")
assert parse_instruction("NOT y -> i") == ("NOT", "y", "i")


insts = utils.import_file("input_sm")
wires_sm = {
    "d": 72,
    "e": 507,
    "f": 492,
    "g": 114,
    "h": 65412,
    "i": 65079,
    "x": 123,
    "y": 456,
}

assert connect_wires(insts) == wires_sm

a_value = assemble_circuit("input")
print(a_value)
