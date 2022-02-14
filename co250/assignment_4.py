import numpy as np
from simplex import canonical_form


def q1_c():
    A = np.array([[1, 0, 0, -1, 0, 0, 1, -1, 1, 1],
                  [1, 1, -1, -2, 1, 0, 0, 1, -1, 0],
                  [0, 1, 0, 0, 1, 0, -1, 0, 0, 0],
                  [0, -2, 2, 0, 0, 0, -1, -1, 2, 2]])
    b = np.array([6, 13, -3, -6])
    c = np.array([0, 4, 1, 3, 3, 1, 0, -4, 5, 2])
    F = slice(0, 4)
    N = slice(4, A.shape[1])
    A_F_inv = np.linalg.inv(A[:, F])
    d = c[N] - np.linalg.multi_dot([c[F], A_F_inv, A[:, N]])
    print(np.dot(A_F_inv, b))
    print(np.linalg.multi_dot([c[F], A_F_inv, b]))


def q2():
    A = np.array([[1, 10, 0, 2, 0],
                  [0, 6, 1, 2, 0],
                  [1, 7, 0, 1, 1]])
    b = np.array([5, 5, 3])
    c = np.array([0, -3, 0, -1, 0])
    B_1 = np.array([2, 4, 5]) - 1
    B_2 = np.array([2, 3, 4]) - 1
    A_prime, b_prime, c_bar, z_bar = canonical_form(A, b, c, B_2)
    print(A_prime)
    print(b_prime)


def q3():
    A = np.array([[-1, 1, -1, 0, 1, 0, 0],
                  [1, -1, 1, -1, 0, 1, 0],
                  [-1, 1, -1, 2, 0, 0, 1]])
    b = np.array([4, 4, 2])
    c = np.array([2, -3, 1, -1, 0, 0, 0])
    B_2 = np.array([1, 4, 5]) - 1  # subtract 1 because of zero indexing
    result = canonical_form(A, b, c, B_2)
    print(result)


def main():
    q3()


if __name__ == '__main__':
    main()
