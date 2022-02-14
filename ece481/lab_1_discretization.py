import sympy as sp


def discretization():
    K_1, tau, T, z = sp.symbols('K_1, tau, T, z')
    s = 2 / T * (z - 1) / (z + 1)
    H = K_1 / (s * (tau * s + 1))
    print(sp.latex(sp.expand(sp.simplify(H))))


if __name__ == '__main__':
    discretization()
