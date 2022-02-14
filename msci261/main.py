import numpy as np


def compounding_factor(P, i, n):
    return P * (1 + i) ** n


def discounting_factor(F, i, n):
    return F / (1 + i) ** n


def compound_amount_factor(A, i, n):
    return A * ((1 + i) ** n - 1) / i


def sinking_fund_factor(F, i, n):
    return F * i / ((1 + i) ** n - 1)


def present_worth_factor(A, i, n):
    return A * ((1 + i) ** n - 1) / (i * (1 + i) ** n)


def capital_recovery_factor(A, i, n):
    return A * (i * (1 + i) ** n) / ((1 + i) ** n - 1)


def gradient_present_worth_factor(G, i, n):
    return G * ((1 + i) ** n - i * n - 1) / (i ** 2 * (1 + i) ** n)


def gradient_uniform_series(G, i, n):
    return G * (1 / i - n / ((1 + i) ** n - 1))


def geometric_gradient_factor(A, i, g, n):
    if i == g:
        return A * n / (1 + i)
    else:
        return A * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)


def depreciation_SOYD(B, S, N, t_vals):
    SOYD = N * (N + 1) / 2
    return sum([(N - t + 1) * (B - S) / SOYD for t in t_vals])


def depreciation_DDB(B, N, t_vals):
    D = 2 / N
    return sum([D * B * (1 - D) ** (t - 1) for t in t_vals])


def depreciation_CCA(S, rate, t_vals, half_year_rule=True):
    d_t = [S * rate / 2 if half_year_rule else S * rate]
    for _ in range(max(t_vals) - 1):
        d_t.append((S - sum(d_t)) * rate)
    return sum([d_t[t - 1] for t in t_vals])


if __name__ == '__main__':
    # print(present_worth_factor(2300, 0.0506, 40) / 2)
    # print(discounting_factor(2300, 0.0506, 40))
    interest = (0.08 - 0.06) / (1 + 0.06)
    print(interest)
    print(present_worth_factor(1, interest, 40))
    print(gradient_present_worth_factor(1600, interest, 40))
    print(discounting_factor(gradient_present_worth_factor(1600, interest, 39), interest, 1))

    print(discounting_factor(gradient_present_worth_factor(2000, interest, 39), interest, 1))
