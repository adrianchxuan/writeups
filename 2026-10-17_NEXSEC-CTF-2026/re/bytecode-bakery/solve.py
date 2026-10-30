# PUSH ; [1]
# PUSH INGREDIENT ; [1, 83]
# PUSH ; [1, 83, 170] X XOR 170 = 196, X = 110
# XOR ; [1, 249]
# PUSH ; [1, 249, 139] X XOR 139 = 79, X = 196
# XOR ; [1, 114] 
# PUSH ; [1, 114, 7]
# CIRCLE SHIFT ; [1, 57] PRE SHIFT = 01001111 (79)
# PUSH ; [1, 57, 221] 202 + 221 = 423 MOD 8 = 10100111 (167) 167,221
# SUB ; [1, 92]
# PUSH ; [1, 92, 202] 
# EQUALS ; [1, 0]
# AND ; [0]

# [64, 0, 108, 52, 83, 124, 18, 2, 5, 27, 60, 39, 59, 87, 74, 11, 20, 57, 43, 68, 94, 49, 59, 87, 88, 95, 86, 61, 106, 92, 54, 108, 71, 13, 27, 61, 106, 4, 89, 28, 15, 77, 4, 81, 6, 22, 11, 29, 11, 196]

#!/usr/bin/env python3
"""The Bytecode Bakery oven.

Usage: python3 oven.py [recipe.bin]

The oven bakes a recipe (bytecode) using the ingredient list (your input).
If the recipe accepts your ingredients, you have found the flag.
"""
import os
import struct
import sys

MAGIC = b"BAKE" #66 65 75 69
MAX_STEPS = 100_000 #100 000 times


class OvenError(Exception):
    pass


def load_recipe(path):
    blob = open(path, "rb").read() 
    if len(blob) < 8 or blob[:4] != MAGIC: 
        raise OvenError("not a recipe file")
    version, input_len, code_len = struct.unpack("<BBH", blob[4:8]) # version 1, input 50, code len: 1143
    if version != 1:
        raise OvenError("unsupported recipe version")
    code = blob[8:8 + code_len]
    REVcode = code[::-1] # reverse entire bytecode so we start from the back
    if len(code) != code_len:
        raise OvenError("truncated recipe")
    # print(REVcode)
    return input_len, REVcode[5:] # shave the opcode bytes used for verifying the flag


def unbake(code):
    stack = []
    addOrsub = 0
    numReversedOp = 0
    pc = 0
    loop = 0
    print(code)
    try:
        for _ in range(MAX_STEPS):
            if not 0 <= pc < len(code):
                raise OvenError(f"the recipe runs off the end at {pc:#06x}")
            op = code[pc]
            pc += 1

            if numReversedOp in (2,5,8,11,14,16,18): # values pushed, we skip these when in reverse order
                if numReversedOp == 18: # end of sequence for one char
                    loop+=1
                    numReversedOp = 0
                numReversedOp += 1
                continue

            if loop == 50:
                print("LOOPED 50 TIMES")
                break

            if op == 0x01:
                print("count:",pc,"; num:", numReversedOp, "; prev push:",code[pc-2], "curr push:", code[pc-1])
                stack.append(code[pc-2]) # PUSH

                if numReversedOp == 6: # REVERSE ADD/SUB
                    print("addorsub:" ,addOrsub)
                    if addOrsub == 0: 
                        b, a = stack.pop(), stack.pop() # REVERSE SUB
                        stack.append((a + b) & 0xFF)
                    else:
                        b, a = stack.pop(), stack.pop() # REVERSE ADD
                        stack.append((a - b) & 0xFF)

                elif (numReversedOp == 9): # REVERSE CIRCLE
                    n, v = stack.pop() & 7, stack.pop()
                    print(n, v)
                    stack.append(((v << (8 - n)) | (v >> n)) & 0xFF) 

                elif ((numReversedOp == 12)): # XOR
                    b, a = stack.pop(), stack.pop()
                    stack.append(a ^ b)
                    
                numReversedOp += 1
                print(stack)
            
            elif op == 0x02:
                # stack.append(ingredients[code[pc]]) # PUSH INPUT
                numReversedOp+=1
                print("count:",pc," ; num:",numReversedOp,"; PUSH INGREDIENT ;")
            
            elif op == 0x03:
                # b, a = stack.pop(), stack.pop() # ADD
                # stack.append((a + b) & 0xFF)
                addOrsub = 1
                numReversedOp += 1
                print("count:",pc," ; num:",numReversedOp,"; ADD ;")
            
            elif op == 0x04:
                # b, a = stack.pop(), stack.pop() # SUB
                # stack.append((a - b) & 0xFF) 
                addOrsub = 0
                numReversedOp += 1
                print("count:",pc," ; num:",numReversedOp,"; SUB ;")
            
            elif op == 0x05:
                # b, a = stack.pop(), stack.pop() # XOR
                # stack.append(a ^ b)

                numReversedOp += 1
                print("count:",pc," ; num:",numReversedOp,"; XOR ;")
            
            elif op == 0x06:
                # n, v = stack.pop() & 7, stack.pop() #CIRCLE UNSHIFT
                # stack.append(((v << n) | (v >> (8 - n)) & 0xFF) 
                numReversedOp += 1
                print("count:",pc," ; num:",numReversedOp,"; CIRCLE SHIFT ;")
            
            elif op == 0x07:
                # b, a = stack.pop(), stack.pop() #EQUAL
                # stack.append(1 if a == b else 0)
                numReversedOp += 1
                print("count:",pc," ; num:",numReversedOp,"; EQUALS ;")
            
            elif op == 0x08:
                # target = code[pc] | (code[pc + 1] << 8) # JNZ (JUMP IF NOT ZERO)
                # pc += 2
                # if stack.pop() != 0:
                #     pc = target

                print("count:",pc," ; num:",numReversedOp,"; JUMP IF NOT XERO ")
            
            elif op == 0x09:
                print("count before op9:",pc)  
                # pc = code[pc] | (code[pc + 1] << 8)
                print("count:",pc," ; num:",numReversedOp,"; TELEPORT? ;")
                print (stack)
                return False
            
            elif op == 0x0A:
                print("count:",pc," ; num:",numReversedOp,"op10 wrong input")
                # return False
            
            elif op == 0x0B:
                print("count:",pc," ; num:",numReversedOp,"op11 corek")
                # return True
            
            elif op == 0x0C:
                stack.append(stack[-1]) # DUP
                print("count:",pc," ; num:",numReversedOp,"; DUPE ;") 
                
            elif op == 0x0D:
                # b, a = stack.pop().pop() # AND
                # stack.append(a & b)
                numReversedOp += 1
                print("count:",pc," ; num:",numReversedOp,"; AND ;") 
            else:
                # raise OvenError(f"unknown opcode {op:#04x} at {pc - 1:#06x}")
                pass
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

    # try:
    #     text = input("Enter ingredient list: ")
    # except EOFError:
    #     return 1
    # ingredients = text.strip().encode("latin-1", "replace")

    # if len(ingredients) != input_len:
    #     print(f"The recipe needs exactly {input_len} ingredients.")
    #     return 1

    try:
        unbaked = unbake(code)
    except OvenError as e:
        print(f"The oven refuses this recipe: {e}")
        return 2
    if unbaked:
        print("Fresh from the oven! Submit your ingredient list as the flag.")
        return 0
    print("The dough collapsed. Try again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
