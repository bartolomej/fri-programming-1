from math import *
import sys

memo = {}


def z(x):
    if x == 0.0:
        return 0
    if memo.get(x):
        return memo.get(x)
    else:
        y = (1664525 * z(x - 1) + 1013904223) % pow(2, 32)
        memo[x] = y
        return y


if __name__ == "__main__":
    sys.setrecursionlimit(1500)
    count = 0
    for i in range(0, 1000):
        if z(i) % 10 == 6:
            count += 1
    print("Ana je bila v sobi s stevilo 6: ", count, "x")
