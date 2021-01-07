from math import *
import sys

memoAna = {}
memoBerta = {}


def ana(x):
    if x == 0.0:
        return 0
    if memoAna.get(x):
        return memoAna.get(x)
    else:
        y = (1664525 * ana(x - 1) + 1013904223) % 2**32
        memoAna[x] = y
        return y


def berta(x):
    if x == 0.0:
        return 0
    if memoBerta.get(x):
        return memoBerta.get(x)
    else:
        y = (22695477 * berta(x - 1) + 1) % 2**32
        memoBerta[x] = y
        return y


if __name__ == "__main__":
    sys.setrecursionlimit(1500)
    count = 0
    for i in range(0, 1000):
        a = ana(i)
        b = berta(i)
        if a % 10 == b % 10:
            count += 1
    print("Ana in Berta sta se srecali: ", count, "x")
