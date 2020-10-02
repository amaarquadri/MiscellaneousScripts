import numpy as np
from src.right_truncatable_primes import is_prime

# https://www.youtube.com/watch?v=AXfl_e33Gt4


def find_prime_pairs(n):
    nums = list(range(1, n + 1))
    while True:
        np.random.shuffle(nums)
        for i in range(len(nums) - 1):
            if not is_prime(nums[i] + nums[i + 1]):
                break
        else:
            return nums


if __name__ == '__main__':
    print(find_prime_pairs(9))
