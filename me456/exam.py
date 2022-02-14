def churchill_bernstein(Re, Pr):
    """
    Estimates the Nusselt number for external flow over a perpendicular cylinder.
    The heat transfer coefficient can then be calculated using h=Nu*k/D
    where k is the thermal conductivity of the fluid, and D is the diameter of the cylinder.
    """
    a = 0.62 * Re ** 0.5 * Pr ** (1 / 3)
    b = (1 + (0.4 / Pr) ** (2 / 3)) ** 0.25
    c = (1 + (Re / 282_000) ** 0.625) ** 0.8
    return 0.3 + (a / b) * c


def main():
    print(churchill_bernstein(31124, 0.705))


if __name__ == '__main__':
    main()
