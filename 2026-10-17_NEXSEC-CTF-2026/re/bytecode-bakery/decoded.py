data = [11, 29, 11, 22, 6, 81, 4, 77, 15, 28, 89, 4, 106, 61, 27, 13, 71, 108, 54, 92, 106, 61, 86, 95, 88, 87, 59, 49, 94, 68, 43, 57, 20, 11, 74, 87, 59, 39, 60, 27, 5, 2, 18, 124, 83, 52, 108, 0, 64]

start_value = 110 # we get this from 169 XOR 170 (value from bytecode)
decrypted = [110]

# The first step: Start value XOR First byte
current_xor = start_value ^ data[0]
decrypted.append(current_xor)

# The rest of the chain: Current byte XOR Previous Decrypted byte
for i in range(1, len(data)):
    current_xor = decrypted[-1] ^ data[i]
    decrypted.append(current_xor)

print(decrypted)

print(bytes(decrypted).decode())