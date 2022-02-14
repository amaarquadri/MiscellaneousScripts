import numpy as np
import sympy as sp
from scipy import optimize


def q2_2():
    c = np.array([2, 1, 0, 3])
    A = np.array([[9, -1, 2, -6],
                     [-2, -1, 0, 5],
                     [-14, 4, -3, 2]])
    b = np.array([1, -6, 1])
    b_prime = np.array([7, 3, -18])
    f = np.array([2, 2, 1])
    g = np.array([1, 3, 0, 1])
    h = np.array([1, 0, 2, 1])
    print(np.dot(f.T, A))
    print(np.dot(A, g))
    print(np.dot(c.T, g))
    print(np.dot(f.T, b))
    print(np.dot(A, h))
    print(np.dot(c.T, h))
    result = optimize.linprog(c, A_eq=A, b_eq=b)
    print(result)
    print(sp.Matrix(np.column_stack((A, b))).rref()[0])


def main():
    q2_2()


if __name__ == '__main__':
    main()
