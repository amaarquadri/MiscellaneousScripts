from math import log
import matplotlib.pyplot as plt
from matplotlib import use
use('TkAgg')


class HereditaryTree:
    """
    Represents a natural number in hereditary notation, independent of the underlying base.
    Stored as a series of coefficients, and corresponding exponents.
    Zero is represented with empty lists.
    """

    def __init__(self, coefficients, exponents):
        self.coefficients = []
        self.exponents = []
        for coefficient, exponent in zip(coefficients, exponents):
            if coefficient != 0:
                self.coefficients.append(coefficient)
                self.exponents.append(exponent)

    def to_int(self, base=2):
        if len(self.coefficients) == 0:
            return 0

        return sum(coefficient * base ** exponent.to_int(base)
                   for coefficient, exponent in zip(self.coefficients, self.exponents))

    @staticmethod
    def parse(value, base=2):
        digits = []
        while value > 0:
            digits.append(value % base)
            value //= base

        exponents = [HereditaryTree.parse(i, base) for i in range(len(digits))]
        return HereditaryTree(digits, exponents)

    def __str__(self):
        if len(self.coefficients) == 0:
            return '0'
        return '+'.join([f'{coefficient}' if len(exponent.coefficients) == 0 else
                         (f'w^({exponent})' if coefficient == 1 else f'{coefficient}*w^({exponent})')
                         for coefficient, exponent in zip(self.coefficients, self.exponents)])


def goodstein_sequence_generator(seed):
    yield seed
    value = seed
    i = 2
    while True:
        value = HereditaryTree.parse(value, i).to_int(i + 1) - 1
        i += 1
        yield value


def plot_sequence(seed=15, terms=1000):
    generator = goodstein_sequence_generator(seed)
    sequence = [next(generator) for _ in range(terms)]

    for i, term in enumerate(sequence[:20]):
        print(f'{term}: {HereditaryTree.parse(term, i + 2)}')

    plt.plot(list(range(terms)), [log(term) for term in sequence])
    plt.title(f'Goodstein Sequence Starting at {seed}')
    plt.xlabel('Term')
    plt.ylabel('Ln(term)')
    plt.show()


if __name__ == '__main__':
    plot_sequence()
