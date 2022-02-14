import sympy as sp


def factor_linear_quadratic(f, x, as_list=False):
    """
    Factors a polynomial f(x) with real coefficients
    into linear and quadratic terms.
    Will not work if f depends on variables other than x.
    Returns a tuple with the constant coefficient and a list of the factors
    if as_list is True.
    """
    factors = []
    origin_roots = 0
    for root, multiplicity in sp.roots(f, x).items():
        if root == 0:
            factors.append((x, multiplicity))
            origin_roots = multiplicity
        elif root.is_real:
            factors.append((x - root, multiplicity))
        elif sp.im(root) > 0:
            factors.append((sp.expand((x - root) *
                                      (x - sp.conjugate(root))),
                            multiplicity))
    coefficient = (f / x ** origin_roots).subs(x, 0) / \
        sp.prod([factor.subs(x, 0) ** multiplicity
                 for factor, multiplicity in factors if factor != x])
    if as_list:
        return coefficient, factors
    return coefficient * sp.prod([factor ** multiplicity
                                  for factor, multiplicity in factors])


def factor_rational_linear_quadratic(f, x, as_list=False):
    """
    Factors a rational function's numerator and denominator
    into linear and quadratic terms.
    Will not work if f depends on variables other than x.
    Returns a tuple with the constant coefficient,
    a list of the numerator factors,
    and a list of the denominator factors if as_list is True.
    """
    num, den = sp.fraction(sp.simplify(f))
    num_coefficient, num_factors = factor_linear_quadratic(num, x,
                                                           as_list=True)
    den_coefficient, den_factors = factor_linear_quadratic(den, x,
                                                           as_list=True)
    coefficient = sp.simplify(num_coefficient / den_coefficient)
    if as_list:
        return coefficient, num_factors, den_factors
    return coefficient * \
        sp.prod([factor ** multiplicity
                 for factor, multiplicity in num_factors]) / \
        sp.prod([factor ** multiplicity
                 for factor, multiplicity in den_factors])


def main():
    s = sp.symbols('s')
    K_1 = 2.09806
    tau = 0.0150167
    K_2 = 0.056444444
    K_3 = -540.865  # cm/s^2
    P = K_1 / (s * (tau * s + 1))
    C = 189.9598704 / (s + 41.584)
    P_2 = C * P / (1 + C * P) * K_2 * K_3 / s ** 2
    P_2 = factor_rational_linear_quadratic(P_2, s)
    print(sp.latex(P_2))
    print(str(P_2).replace('**', '^'))


if __name__ == '__main__':
    main()
