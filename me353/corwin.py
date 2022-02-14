import numpy as np
from scipy import optimize


def q_flux_conv(h, Ts, T8):
    return h * (Ts - T8)


def q_conv(area, h, Ts, T8):
    return q_flux_conv(h, Ts, T8) * area


class FinSolver:
    def __init__(self, h, k, area, perimeter, eff):
        self.h = h
        self.k = k
        self.perimeter = perimeter
        self.area = area
        self.eff = eff

    def straight_fin(self, low_bound, high_bound):
        m = np.sqrt(self.h * self.perimeter / (self.k * self.area))
        f = lambda L: self.eff - np.tanh(m * L) / (m * L)
        return optimize.bisect(f, low_bound, high_bound)


class FinConsts:
    def __init__(self, Tb, T8, h, k, L, diameter=0, thickness=0, width=0):
        self.theta_b = Tb - T8
        self.L = L
        self.h = h
        self.k = k
        self.thickness = thickness
        self.width = width
        self.diameter = diameter
        self.area = np.pi / 4 * diameter ** 2 + thickness * width
        self.perimeter = np.pi * diameter * L + 2 * width * thickness
        self.Tb = Tb
        self.T8 = T8
        self.m = np.sqrt(h * self.perimeter / (k * self.area))
        self.M = np.sqrt(h * k * self.perimeter * self.area) * self.theta_b

    def q_flux_conv(self):
        return self.h * self.theta_b

    def q_conv(self):
        return q_flux_conv(self) * self.area

    def fin_q_conv(self):
        return self.M * (np.sinh(self.m * self.L) + (self.h / (self.m * self.k)) *
                         np.cosh(self.m * self.L)) / (np.cosh(self.m * self.L) +
                                                      (self.h / (self.m * self.k)) * np.sinh(self.m * self.L))

    def fin_q_adiabatic(self):
        return self.M * np.tanh(self.m * self.L)

    def fin_q_inf(self):
        return self.M

    def fin_q_temp(self, TL):
        theta_L = TL - self.T8
        return self.M * (np.cosh(self.m * self.L) - theta_L / self.theta_b) / \
               np.sinh(self.m * self.L)

    def fin_q_annular(self, diameter):
        Lc = self.L + self.thickness / 2
        rc = diameter / 2 + Lc
        Ap = Lc * self.thickness
        mLc = (2 * self.h * Lc ** 3 / (self.k * Ap)) ** (1 / 2)
        eff = np.tanh(mLc) / mLc
        return eff * 2 * np.pi * self.h * self.theta_b * (rc ** 2 - diameter ** 2 / 4)


class LumpedConsts:
    def __init__(self, Ti, Tf, T8, specific_heat, density, k, h,
                 sphere_diameter=0.0, cylinder_diameter=0.0, wall_length=0.0):
        self.Ti = Ti
        self.Tf = Tf
        self.T8 = T8
        self.h = h
        self.k = k
        self.c = specific_heat
        self.rho = density
        self.wall_length = wall_length
        self.Lc = sphere_diameter / 6 + cylinder_diameter / 4 + wall_length / 2
        # self.mass = density * (4 * np.pi / 3 * sphere_diameter ** 3 / 8 +
        #                        np.pi / 4 * cylinder_diameter ** 2 * cylinder_length +
        #                        wall_length * wall_width * wall_thickness) \
        #             + mass
        self.rho = density
        self.V = 4 * np.pi / 3 * sphere_diameter ** 3 / 8 +\
                               cylinder_diameter / 4 +\
                               wall_length
        # self.As = np.pi * sphere_diameter ** 2 + \
        #           np.pi * (cylinder_diameter ** 2 / 2 + cylinder_diameter * cylinder_length) + \
        #           2 * (wall_width * wall_thickness + wall_width * wall_length + wall_thickness * wall_length)
        self.As = np.pi * sphere_diameter ** 2 + \
                  (cylinder_diameter > 0) + \
                  (wall_length > 0)

    def find_time(self):
        Bi = self.h * self.Lc / self.k
        print('Bi is ' + str(Bi))
        if Bi < 0.1:
            return np.log((self.Tf - self.T8) / (self.Ti - self.T8)) * \
                   -self.c * self.rho * self.V / (self.h * self.As)
        else:
            alpha = self.k / (self.rho * self.c)
            f = lambda x: Bi - x * np.tan(x)
            zeta = optimize.bisect(f, 0.3, 1.5)
            print('zeta is ' + str(zeta))
            C1 = 4 * np.sin(zeta) / (2 * zeta + np.sin(2 * zeta))
            print('C1 is ' + str(C1))
            return np.log((self.Tf - self.T8) / (C1 * (self.Ti - self.T8))) * \
                   -(self.wall_length/2 / zeta) ** 2 / alpha

    def find_h(self, t):
        return np.log((self.Tf - self.T8) / (self.Ti - self.T8)) * \
               -self.c * self.rho * self.V / (t * self.As)

    def find_temp(self, t):
        return (self.Ti - self.T8) * np.exp(-self.h * self.As * t /
                                            (self.c * self.rho * self.V))\
               + self.T8


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = LumpedConsts(300, 550, 700, 500, 7800, 45, 500, wall_length=100E-3)
    print(a.find_time())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
