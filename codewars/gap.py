from gmpy2 import next_prime as np


def gap(g, m, n):
    m = s = np(m - 1)
    while m <= n:
        m = np(m)
        if m - s == g:
            return [s, m]
        s = m
    return None


print(gap(2, 100, 110))
