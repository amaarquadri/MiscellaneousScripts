import sympy as sp


def linearize():
    theta = sp.symbols('theta', real=True)
    L, l, r = sp.symbols('L, l, r', real=True, positive=True)
    delta_x = L - r * (1 - sp.cos(theta))
    delta_y = l - r * sp.sin(theta)
    d = sp.sqrt(delta_x ** 2 + delta_y ** 2)
    alpha = sp.acos((L ** 2 + d ** 2 - l ** 2) / (2 * L * d))
    beta = sp.atan(delta_y / delta_x)
    phi = alpha - beta
    K_2 = sp.diff(phi, theta).subs(theta, 0)
    print(sp.simplify(K_2))


if __name__ == '__main__':
    linearize()
