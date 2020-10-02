from math import sqrt, ceil


def is_prime(n):
    if n == 2 or n == 3:
        return True

    if n < 5 or n % 2 == 0 or n % 3 == 0:
        return False

    # check divisibility by numbers that are equal to 1 mod 6 or 5 mod 6.
    # This avoids redundancy with checking divisibility mod 2 and divisibility mod 3.
    for k in range(1, ceil((sqrt(n) + 1) / 6)):
        if n % (6 * k - 1) == 0 or n % (6 * k + 1) == 0:
            return False

    return True


def generate_right_truncatable_primes():
    candidates = [n for n in range(10) if is_prime(n)]
    digits = [1, 3, 7, 9]  # don't include even digits or 5 due to divisibility by 2 and 5 respectively
    results = []

    while len(candidates) > 0:
        print(len(candidates))
        new_candidates = []
        for candidate in candidates:
            longer_candidates = [n for n in [10 * candidate + d for d in digits] if is_prime(n)]
            if len(longer_candidates) == 0:
                results.append(candidate)
            else:
                new_candidates += longer_candidates
        candidates = new_candidates

    return sorted(results)


def generate_left_truncatable_primes():
    candidates = [n for n in range(10) if is_prime(n)]
    digits = list(range(1, 10))
    results = []

    while len(candidates) > 0:
        print(len(candidates))
        print(candidates)
        new_candidates = []
        for candidate in candidates:
            longer_candidates = [n for n in [int(str(d) + str(candidate)) for d in digits] if is_prime(n)]
            if len(longer_candidates) == 0:
                results.append(candidate)
            else:
                new_candidates += longer_candidates
        candidates = new_candidates

    return sorted(results)


if __name__ == '__main__':
    print(generate_left_truncatable_primes())
