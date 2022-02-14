import numpy as np
from matplotlib import pyplot as plt


def remy_sigrist_generator():
    """
    n^2
    """
    a = []
    while True:
        illegals = {value for i, value in enumerate(a) if i & len(a)}
        a_n = 0
        while a_n in illegals:
            a_n += 1
        a.append(a_n)
        yield a_n


def hofstadters_q_sequence():
    """
    n
    """
    yield 1
    yield 1
    a = [1, 1]
    while True:
        n = len(a)
        a_n = a[n - a[n - 1]] + a[n - a[n - 2]]
        yield a_n
        a.append(a_n)


def forest_fire_sequence():
    """
    n^2
    """
    a = []
    while True:
        n = len(a)
        illegals = {2 * a[n - j] - a[n - 2 * j] for j in range(1, n // 2)}
        a_n = 1
        while a_n in illegals:
            a_n += 1
        yield a_n
        a.append(a_n)
        n += 1


def gcd(a, b):
    if b > a:
        a, b = b, a
    while b > 0:
        a, b = b, a % b
    return a


def fly_straight_dammit():
    yield 1
    yield 1
    a = [1, 1]
    while True:
        n = len(a)
        div = gcd(n, a[n - 1])
        a_n = (a[n - 1] + n + 1) if div == 1 else (a[n - 1] // div)
        yield a_n
        a.append(a_n)


def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 5:
        return False
    if n % 2 == 0 or n % 3 == 0:
        return False
    for k in range(1, 1 + int((np.sqrt(n) + 1) / 6)):
        if n % (6 * k - 1) == 0 or n % (6 * k + 1) == 0:
            return False
    return True


def prime_generator():
    def potential_primes():
        yield 2
        yield 3
        k = 1
        while True:
            yield 6 * k - 1
            yield 6 * k + 1
            k += 1

    def div_check(m):
        return lambda n: n % m != 0

    iterator = potential_primes()
    while True:
        p = next(iterator)
        yield p
        iterator = filter(div_check(p), iterator)


def prime_rectangles():
    def reverse_bits(n):
        bits = []
        k = 1
        while k <= n:
            bits.append(n & k)
            k *= 2

        reversed_n = 0
        k = 1
        for bit in bits[::-1]:
            if bit:
                reversed_n += k
            k *= 2
        return reversed_n

    return map(lambda p: p - reverse_bits(p), prime_generator())


def van_eck():
    # youtu.be/watch?v=etMJxB-igrc
    yield 0
    a = [0]
    while True:
        where = np.argwhere(np.array(a[:-1]) == a[-1])
        if len(where) == 0:
            yield 0
            a.append(0)
        else:
            a_n = len(a) - 1 - np.max(where)
            yield a_n
            a.append(a_n)


def main():
    generator = van_eck()
    sequence = [next(generator) for _ in range(1_000)]
    print(sequence)
    plt.scatter(np.arange(len(sequence)), sequence, s=2, alpha=1)
    plt.xlabel('n')
    plt.ylabel('a(n)')
    plt.show()


if __name__ == '__main__':
    main()
