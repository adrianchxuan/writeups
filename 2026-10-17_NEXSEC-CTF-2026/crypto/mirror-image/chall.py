import signal
import sys
from hashlib import sha256
from secrets import randbelow, randbits, token_bytes

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MIRRORS = 112          
BITS = 16              
SHADOWS = 2            
CASTER = 1024          
LIMIT = 120


def hall(lo, hi):
    sieve = bytearray([1]) * (hi + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(hi ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(range(i * i, hi + 1, i)))
    return [p for p in range(lo, hi + 1) if sieve[p]]


def pick(pool, count):
    pool = list(pool)
    return [pool.pop(randbelow(len(pool))) for _ in range(count)]


def shuffle(xs):
    for i in range(len(xs) - 1, 0, -1):
        j = randbelow(i + 1)
        xs[i], xs[j] = xs[j], xs[i]


def main():
    flag = open("flag.txt").read().strip().encode()
    mirrors = pick(hall(1 << (BITS - 1), (1 << BITS) - 1), MIRRORS)
    s = randbits(CASTER)

    print("The archmage steps into the hall of mirrors and casts Mirror Image.")
    print("Each mirror throws back a few shadows; exactly one shadow per mirror is the real one.")
    for m in mirrors:
        shadows = [s % m]
        while len(shadows) < SHADOWS:
            r = randbelow(m)
            if r not in shadows:
                shadows.append(r)
        shuffle(shadows)
        print("mirror =", (m, tuple(shadows)))

    key = sha256(s.to_bytes(CASTER // 8, "big")).digest()
    nonce = token_bytes(12)
    print("ward =", (nonce.hex(), AESGCM(key).encrypt(nonce, flag, None).hex()))
    sys.stdout.flush()


if __name__ == "__main__":
    signal.alarm(LIMIT)
    main()
