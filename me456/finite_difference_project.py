import numpy as np
from numpy import ma
import sympy as sp
from matplotlib import pyplot as plt, use, tri
import pickle
from time import time

use('TkAgg')


def get_node_count(n):
    return (4 * n + 1) * (3 * n) + (16 * n + 1) * (1 * n + 1)


def get_index(n, row, column):
    """
    Returns the index of the node corresponding to the given row and column.
    Row zero, column zero corresponds to the top left corner of the region.
    """
    if row < 0 or column < 0:
        raise ValueError('Row and column must be non-negative!')
    if row < 3 * n:
        if column > 4 * n:
            raise ValueError('Column is out of bounds!')
        return (4 * n + 1) * row + column
    elif row <= 4 * n:
        if column > 16 * n:
            raise ValueError('Column is out of bounds!')
        return (4 * n + 1) * (3 * n) + (16 * n + 1) * (row - 3 * n) + column
    else:
        raise ValueError('Row is out of bounds!')


def get_row_column(n, index):
    """
    Returns the row and column of the node at the given index.
    This is the inverse function of get_index.
    """
    if index < 0:
        raise ValueError('Index must be non-negative!')

    if index < (4 * n + 1) * (3 * n):
        return index // (4 * n + 1), index % (4 * n + 1)
    else:
        index -= (4 * n + 1) * (3 * n)
        return 3 * n + index // (16 * n + 1), index % (16 * n + 1)


def test_consistency():
    for n in range(2, 17):
        for i in range(get_node_count(n)):
            assert i == get_index(n, *get_row_column(n, i))


def solve(n, h, k):
    """
    :param n: Regions per mm. Must be at least 2.
    :param h: Convective heat transfer coefficient in W/(mm^2*K).
    :param k: Thermal conductivity in W/(mm*K).
    """
    if n < 2:
        raise ValueError('n must be at least 2!')

    delta_x = 1 / n  # mm
    node_count = get_node_count(n)
    Bi = h * delta_x / k

    A = np.zeros((node_count, node_count))
    b = np.zeros(node_count)

    # Interior points
    for row in range(1, 4 * n):
        for column in range(1, (4 if row <= 3 * n else 16) * n):
            index = get_index(n, row, column)
            A[index, index] = 1
            A[index, get_index(n, row - 1, column)] = -0.25  # north
            A[index, get_index(n, row, column + 1)] = -0.25  # east
            A[index, get_index(n, row + 1, column)] = -0.25  # south
            A[index, get_index(n, row, column - 1)] = -0.25  # west

    # Left boundary
    for row in range(0, 4 * n + 1):
        index = get_index(n, row, 0)
        A[index, index] = 1
        b[index] = 100  # deg C

    # Left section of top boundary
    for column in range(1, 4 * n):
        index = get_index(n, 0, column)
        A[index, index] = 2
        A[index, get_index(n, 1, column)] = -1  # south
        A[index, get_index(n, 0, column + 1)] = -0.5  # east
        A[index, get_index(n, 0, column - 1)] = -0.5  # west

    # Right section of top boundary
    for column in range(4 * n + 1, 16 * n):
        index = get_index(n, 3 * n, column)
        A[index, index] = 2 + Bi
        A[index, get_index(n, 3 * n + 1, column)] = -1  # south
        A[index, get_index(n, 3 * n, column + 1)] = -0.5  # east
        A[index, get_index(n, 3 * n, column - 1)] = -0.5  # west
        b[index] = 30 * Bi  # deg C

    # Bottom boundary
    for column in range(1, 16 * n):
        index = get_index(n, 4 * n, column)
        A[index, index] = 2
        A[index, get_index(n, 4 * n - 1, column)] = -1  # north
        A[index, get_index(n, 4 * n, column + 1)] = -0.5  # east
        A[index, get_index(n, 4 * n, column - 1)] = -0.5  # west

    # Right boundary
    for row in range(1, 4 * n):
        if row == 3 * n:
            # Skip the two special points
            continue
        column = 4 * n if row < 3 * n else 16 * n
        index = get_index(n, row, column)
        A[index, index] = 2 + Bi
        A[index, get_index(n, row, column - 1)] = -1  # west
        A[index, get_index(n, row - 1, column)] = -0.5  # north
        A[index, get_index(n, row + 1, column)] = -0.5  # south
        b[index] = 30 * Bi  # deg C

    # Topmost point of right boundary
    index = get_index(n, 0, 4 * n)
    A[index, index] = 2 + Bi
    A[index, get_index(n, 0, 4 * n - 1)] = -1  # west
    A[index, get_index(n, 1, 4 * n)] = -1  # south
    b[index] = 30 * Bi  # deg C

    # Bottommost point of right boundary
    index = get_index(n, 4 * n, 16 * n)
    A[index, index] = 2 + Bi
    A[index, get_index(n, 4 * n, 16 * n - 1)] = -1  # west
    A[index, get_index(n, 4 * n - 1, 16 * n)] = -1  # north
    b[index] = 30 * Bi  # deg C

    # Inner corner point
    index = get_index(n, 3 * n, 4 * n)
    A[index, index] = 3 + Bi
    A[index, get_index(n, 3 * n + 1, 4 * n)] = -1  # south
    A[index, get_index(n, 3 * n, 4 * n - 1)] = -1  # west
    A[index, get_index(n, 3 * n - 1, 4 * n)] = -0.5  # north
    A[index, get_index(n, 3 * n, 4 * n + 1)] = -0.5  # east
    b[index] = 30 * Bi  # deg C

    # Outer corner point
    index = get_index(n, 3 * n, 16 * n)
    A[index, index] = 1 + Bi
    A[index, get_index(n, 3 * n + 1, 16 * n)] = -0.5  # south
    A[index, get_index(n, 3 * n, 16 * n - 1)] = -0.5  # west
    b[index] = 30 * Bi  # deg C

    # Solve
    T, *_ = np.linalg.lstsq(A, b, rcond=None)
    print(f'Root Mean Square of Residuals: {np.sqrt(sum((np.dot(A, T) - b) ** 2))}')
    return T


def plot(n, T):
    node_count = get_node_count(n)
    y_vals, x_vals = list(zip(*[get_row_column(n, i) for i in range(node_count)]))
    x_vals = np.array(x_vals) / n
    y_vals = 4 - np.array(y_vals) / n
    triang = tri.Triangulation(x_vals, y_vals)
    interpolator = tri.LinearTriInterpolator(triang, T)
    xi = np.linspace(0, 16, 4000)
    yi = np.linspace(0, 4, 1000)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)
    zi[zi.shape[0] // 4:, zi.shape[1] // 4:] = ma.masked
    fig, ax = plt.subplots()
    cntr1 = ax.contourf(xi, yi, zi, levels=1000, cmap="RdBu_r")
    fig.colorbar(cntr1, ax=ax, label=r'Temperature (${\degree}$ C)')
    ax.set(xlim=(0, 16), ylim=(0, 4))
    ax.set_title(r'Temperature Distribution for $n=' + str(n) + 'mm^{-1}$')
    ax.set_xlabel('Horizontal Position (mm)')
    ax.set_ylabel('Vertical Position (mm)')
    plt.subplots_adjust(hspace=0.5)
    plt.show()


def richardson_extrapolation(n_vals, T_vals):
    delta_x_vals = [1 / n for n in n_vals]
    alpha, p, T_exact = sp.symbols('alpha, p, T_exact', real=True)

    result = sp.solve([sp.Eq(T_exact, T + alpha * delta_x ** p) for delta_x, T in zip(delta_x_vals, T_vals)])
    print(result)
    return result[0][T_exact]


def get_energy_input(n, T, h, k, net=True):
    """
    Calculates the net energy input into the metal (which should be 0) if net=True.
    Calculates the energy transfer through the metal if net=False.
    """
    delta_x = 1 / n
    P_total = 0  # K=W/mm, total power input per unit depth into the page

    # Left boundary (not including endpoints)
    for row in range(1, 4 * n):
        index = get_index(n, row, 0)
        neighbour_index = get_index(n, row, 1)
        P_total += k * (T[index] - T[neighbour_index])

    # Topmost point of left boundary
    index = get_index(n, 0, 0)
    neighbour_index = get_index(n, 0, 1)
    P_total += k * (1 / 2) * (T[index] - T[neighbour_index])

    # Bottommost point of left boundary
    index = get_index(n, 4 * n, 0)
    neighbour_index = get_index(n, 4 * n, 1)
    P_total += k * (1 / 2) * (T[index] - T[neighbour_index])

    if not net:
        return P_total

    # Right section of top boundary
    for column in range(4 * n + 1, 16 * n):
        index = get_index(n, 3 * n, column)
        P_total -= h * delta_x * (T[index] - 30)

    # Right boundary
    for row in range(1, 4 * n):
        if row == 3 * n:
            # Skip the two special points
            continue
        column = 4 * n if row < 3 * n else 16 * n
        index = get_index(n, row, column)
        P_total -= h * delta_x * (T[index] - 30)

    # Topmost point of right boundary
    index = get_index(n, 0, 4 * n)
    P_total -= h * (delta_x / 2) * (T[index] - 30)

    # Bottommost point of right boundary
    index = get_index(n, 4 * n, 16 * n)
    P_total -= h * (delta_x / 2) * (T[index] - 30)

    # Inner corner point
    index = get_index(n, 3 * n, 4 * n)
    P_total -= h * delta_x * (T[index] - 30)

    # Outer corner point
    index = get_index(n, 3 * n, 16 * n)
    P_total -= h * delta_x * (T[index] - 30)

    return P_total


def benchmark(h, k):
    start_time = time()
    solve(2, h, k)
    solve(4, h, k)
    solve(8, h, k)
    time_248 = time() - start_time

    start_time = time()
    solve(16, h, k)
    time16 = time() - start_time
    print(f'n=16 took {time16 / time_248} times longer than n=2, 4, and 8.')


def main():
    test_consistency()

    h = 20 * 10 ** -6  # W/(mm^2*K)
    k = 100 * 10 ** -3  # W/(mm*K)

    # calculate solutions for 2<=n<=16
    n_vals = np.array(list(range(2, 17)))
    T_vals = [solve(n, h, k) for n in n_vals]
    T_corner_vals = np.array([T[get_index(n, 3 * n, 4 * n)] for n, T in zip(n_vals, T_vals)])

    # plot solutions for n=2 and n=16
    plot(n_vals[0], T_vals[0])
    plot(n_vals[-1], T_vals[-1])

    print(f'Power Transfer for n={n_vals[0]}: {get_energy_input(n_vals[0], T_vals[0], h, k, net=False)} W/mm')
    print(f'Power Transfer for n={n_vals[-1]}: {get_energy_input(n_vals[-1], T_vals[-1], h, k, net=False)} W/mm')

    net_energy_inputs = np.array([get_energy_input(n, T, h, k, net=True) for n, T in zip(n_vals, T_vals)])
    print(f'Largest Net Power Discrepancy: {max(abs(net_energy_inputs))} W/mm')

    # Richardson extrapolation with n=2, n=4, and n=8
    T_corner_exact = richardson_extrapolation(n_vals[[0, 2, 6]], T_corner_vals[[0, 2, 6]])

    # Grid refinement study
    plt.scatter(n_vals, T_corner_vals, label='Grid Refinement')
    plt.plot([n_vals[0], n_vals[-1]], 2 * [T_corner_exact], label='Richardson Extrapolation', c='red')
    plt.xlabel(r'Grid Resolution, $n=\frac{1}{{\Delta}x}[mm^{-1}]$')
    plt.ylabel(r'Inner Corner Temperature [${\degree}C$]')
    plt.legend()
    plt.plot()
    plt.show()

    # Run the Richardson extrapolation comparative benchmark
    benchmark(h, k)


if __name__ == '__main__':
    main()
