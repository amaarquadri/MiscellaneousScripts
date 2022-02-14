import numpy as np
from scipy import optimize


def q1_2():
    c = np.array([550, 600, 350, 400, 200])
    A_ub = np.array([[6, 10, 0, 9, 6],
                     [10, 8, 19, 0, 0],
                     [1, 1, 1, 1, 1]])
    b_ub = np.array([60, 80, 32])
    result = optimize.linprog(-c, A_ub, b_ub)
    print(result.x)


def q1_4():
    c = np.array([550, 600, 350, 400, 200])
    A_ub = np.array([[6, 10, 0, 9, 6],
                     [10, 8, 19, 0, 0],
                     [42, 48, 39, 38, 32]])
    b_ub = np.array([60, 80, 640])
    result = optimize.linprog(-c, A_ub, b_ub)
    print(result.x)


def main():
    # q1_2()
    q1_4()


if __name__ == '__main__':
    main()
