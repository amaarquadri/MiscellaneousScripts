import sympy as sp


def q1():
    s, z = sp.symbols('s, z')
    T = sp.symbols('T', real=True, positive=True)
    C = 3 * (s + 1) / (s + 20)
    print(sp.simplify(C.subs(s, 1 / T * (z - 1))))


def q2():
    t = sp.symbols('t', real=True)
    k = sp.symbols('k', real=True, integer=True)
    s, z = sp.symbols('s, z')
    T = sp.symbols('T', real=True, positive=True)
    C = 5 * (s + 1) / (s + 10)
    print('Left Side Rule:', sp.simplify(C.subs(s, 1 / T * (z - 1))))
    C_d = zoh_discretization(t, k, s, z, T, C)
    print(sp.latex(sp.expand(C_d)))


def z_transform(k, z, h):
    if isinstance(h, sp.Add):
        return sum([z_transform(k, z, term) for term in h.args])

    if h.is_constant():
        return h * z / (z - 1)

    if sp.diff(h, k, 2) == 0:
        coefficient = sp.diff(h, k)
        # h = coefficient * k
        return coefficient * z / (z - 1) ** 2

    log_h = sp.expand(sp.log(h))
    if sp.diff(log_h, k, 2) == 0:
        base = sp.exp(sp.diff(log_h, k))
        coefficient = sp.exp(log_h.subs(k, 0))
        # h = coefficient * base ^ k
        return coefficient * z / (z - base)

    raise NotImplementedError


def zoh_discretization(t, k, s, z, T, P):
    pfe = sp.apart(P / s)
    terms = pfe.args if isinstance(pfe, sp.Add) else [pfe]
    terms = [sp.inverse_laplace_transform(term, s, t).subs(t, k * T) for term in terms]
    terms = [term.subs(sp.Heaviside(T * k), 1) for term in terms]
    return (z - 1) / z * z_transform(k, z, sum(terms))


if __name__ == '__main__':
    q2()
