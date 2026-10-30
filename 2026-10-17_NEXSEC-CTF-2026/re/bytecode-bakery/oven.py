#!/usr/bin/env python3
"""The Bytecode Bakery oven.

Usage: python3 oven.py [recipe.bin]

The oven bakes a recipe (bytecode) using the ingredient list (your input).
If the recipe accepts your ingredients, you have found the flag.
"""
import os
import struct
import sys

MAGIC = b"BAKE"
MAX_STEPS = 100_000


class OvenError(Exception):
    pass


def load_recipe(path):
    blob = open(path, "rb").read()
    if len(blob) < 8 or blob[:4] != MAGIC:
        raise OvenError("not a recipe file")
    version, input_len, code_len = struct.unpack("<BBH", blob[4:8])
    if version != 1:
        raise OvenError("unsupported recipe version")
    code = blob[8:8 + code_len]
    if len(code) != code_len:
        raise OvenError("truncated recipe")
    return input_len, code


def bake(code, ingredients):
    stack = []
    pc = 0
    try:
        for _ in range(MAX_STEPS):
            if not 0 <= pc < len(code):
                raise OvenError(f"the recipe runs off the end at {pc:#06x}")
            op = code[pc]
            pc += 1

            if op == 0x01:
                stack.append(code[pc])  # PUSH
                pc += 1
            elif op == 0x02:
                stack.append(ingredients[code[pc]]) # PUSH INGREDIENT
                pc += 1
            elif op == 0x03:
                b, a = stack.pop(), stack.pop() # ADD
                stack.append((a + b) & 0xFF)
            elif op == 0x04:
                b, a = stack.pop(), stack.pop() # SUB
                stack.append((a - b) & 0xFF)
            elif op == 0x05:
                b, a = stack.pop(), stack.pop() # XOR
                stack.append(a ^ b)
            elif op == 0x06:
                n, v = stack.pop() & 7, stack.pop() # CIRCULAR ROTATE
                stack.append(((v << n) | (v >> (8 - n))) & 0xFF)
            elif op == 0x07:
                b, a = stack.pop(), stack.pop() # COMPARE
                stack.append(1 if a == b else 0)
            elif op == 0x08:
                target = code[pc] | (code[pc + 1] << 8) # JNZ (JUMP IF NOT ZERO)
                pc += 2
                if stack.pop() != 0:
                    pc = target
            elif op == 0x09: 
                pc = code[pc] | (code[pc + 1] << 8) # JUMP (TELEPORT)
            elif op == 0x0A: 
                return False # WRONG FLAG
            elif op == 0x0B:
                return True  # CORRECT FLAG
            elif op == 0x0C:
                stack.append(stack[-1]) # DUPE
            elif op == 0x0D:
                b, a = stack.pop(), stack.pop() # AND
                stack.append(a & b)
            else:
                raise OvenError(f"unknown opcode {op:#04x} at {pc - 1:#06x}")
    except IndexError:
        raise OvenError(f"malformed recipe near {pc - 1:#06x}") from None
    raise OvenError("the oven overheated (step limit)")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "recipe.bin")
    try:
        input_len, code = load_recipe(path)
    except (OSError, OvenError) as e:
        print(f"The oven refuses this recipe: {e}")
        return 2

    try:
        text = input("Enter ingredient list: ")
    except EOFError:
        return 1
    ingredients = text.strip().encode("latin-1", "replace")

    if len(ingredients) != input_len:
        print(f"The recipe needs exactly {input_len} ingredients.")
        return 1

    try:
        baked = bake(code, ingredients)
    except OvenError as e:
        print(f"The oven refuses this recipe: {e}")
        return 2
    if baked:
        print("Fresh from the oven! Submit your ingredient list as the flag.")
        return 0
    print("The dough collapsed. Try again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
