import sympy as sp


def lumped_capacitance():
    T, T_inf, T_i, h, A_s, c, rho, V, t = sp.symbols('T, T_inf, T_i, h, A_s, c, rho, V, t')
    tau = c * rho * V / (h * A_s)
    eq = sp.Eq((T - T_inf) / (T_i - T_inf), sp.exp(- t / tau))
    eq = eq.subs({T_inf: 300, T_i: 1000, h: 10, A_s: 2 * sp.pi * 2,
                  c: 140, rho: 1000, V: sp.pi * 3 ** 2, t: 100})
    print(sp.solve(eq, T)[0].evalf())


def center_line_diffusion():
    T, T_inf, T_i, C_1, zeta_1, alpha, L, t = sp.symbols('T, T_inf, T_i, C_1, zeta_1, alpha, L, t')
    F_0 = alpha * t / L ** 2
    eq = sp.Eq((T - T_inf) / (T_i - T_inf), C_1 * sp.exp(- zeta_1 ** 2 * F_0))
    eq = eq.subs({T_inf: 300, T_i: 1000, C_1: 1.02, zeta_1: 0.5, alpha: 13, L: 10, t: 100})
    print(sp.solve(eq, T)[0].evalf())


def center_line_heat_transfer():
    Q, T_inf, T_i, C_1, zeta_1, c_p, rho, V, L, t = sp.symbols(
        'Q, T, T_inf, T_i, C_1, zeta_1, c_p, rho, V, L, t')
    Q_0 = rho * c_p * V * (T_i - T_inf)
    eq = sp.Eq(Q / Q_0, 1 - sp.sin(zeta_1) / zeta_1 * (T - T_inf) / (T_i - T_inf))
    eq = eq.subs({T_inf: 300, T_i: 1000, C_1: 1.02, zeta_1: 0.5, L: 10, t: 100})
    print(sp.solve(eq, Q)[0].evalf())


if __name__ == '__main__':
    center_line_diffusion()
