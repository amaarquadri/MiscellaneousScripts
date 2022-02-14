import sympy as sp


def to_word(expr):
    return sp.latex(expr) \
        .replace(r"\frac{d}{d t} x{\left(t \right)}", r"\dot{x}") \
        .replace(r"\frac{d}{d t} \theta{\left(t \right)}", r"\dot{\theta}") \
        .replace(r"x{\left(t \right)}", "x") \
        .replace(r"theta(t){\left(t \right)}", r"\theta")


def main():
    M, m, b, L, I, g, t = sp.symbols('M, m, b, L, I, g, t')
    x = sp.Function('x')(t)
    x_dot = sp.diff(x, t)
    x_ddot = sp.diff(x_dot, t)
    theta = sp.Function('theta')(t)
    theta_dot = sp.diff(theta, t)
    theta_ddot = sp.diff(theta_dot, t)
    f = sp.Function('f')(t)
    eq1 = sp.Eq(
        (M + m) * x_ddot + b * x_dot + m * L * theta_ddot * sp.cos(theta) - m * L * theta_dot ** 2 * sp.sin(theta), f)
    eq2 = sp.Eq((I + m * L ** 2) * theta_ddot + m * g * L * sp.sin(theta), -m * L * x_ddot * sp.cos(theta))
    result = sp.solve([eq1, eq2], [x_ddot, theta_ddot])
    print(to_word(sp.simplify(result[x_ddot])))
    print(to_word(sp.simplify(result[theta_ddot])))


if __name__ == '__main__':
    main()
