import sympy as sp


def page_189():
    z = sp.symbols('z')
    C = 1/(z-1)
    P_1 = z/(z+0.5)
    P_2 = (z + 1) / (z + 2)
    X = C * P_1 / (1 + 2 * C * P_1)
    H = X * P_2 / (1 + 3 * X * P_2)
    print(sp.simplify(H))


def page_273():
    z, s = sp.symbols('z, s')
    K = sp.symbols('K', real=True)
    H = z ** 2 - 1.1 * z + K
    print(sp.expand(sp.simplify(H.subs(z, (s + 1) / (s - 1)) ** -1)))


if __name__ == '__main__':
    page_273()
