import sympy as sp


def q5():
    s, z = sp.symbols('s, z')
    T = sp.symbols('T', real=True, positive=True)
    C = (3 * s + 8) / s
    print('left hand', sp.simplify(C.subs(s, 1 / T * (z - 1))))
    print('right hand', sp.simplify(C.subs(s, 1 / T * (z - 1) / z)))
    print('trapezo hand', sp.simplify(C.subs(s, 2 / T * (z - 1) / (z + 1))))


def q3():
    s, z = sp.symbols('s, z')
    T = 0.2
    C = 1 / (s ** 2 + 16)
    D = C.subs(s, 1 / T * (z - 1) / z)
    print(sp.simplify(D))


def q2():
    z = sp.symbols('z')
    K, a = sp.symbols('K, a', real=True)
    R = z / (z - 1)
    C = K / (z - a)
    P = 1 / (z * (z - 0.5))
    H = 1 / (1 + C * P)
    print(sp.simplify(sp.limit((z - 1) * H * R, z, 1)))


if __name__ == '__main__':
    q3()
