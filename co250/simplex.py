import numpy as np


def canonical_form(A, b, c, B):
    """
    Converts the given linear program into canonical form for basis B.
    The original linear program is:
    Maximize c^T*x, subject to A*x = b, x >= 0.
    The linear program in canonical form is
    Maximize c_bar^T*x+z_bar, subject to A'*x = b',x >= 0
    where A'_B = I, c_bar_B = 0

    :param B A Python list of indices representing the basis
    :returns A', b', c_bar, z_bar
    """
    A_B_inv = np.linalg.inv(A[:, B])
    A_prime = np.dot(A_B_inv, A)
    b_prime = np.dot(A_B_inv, b)
    y = np.dot(A_B_inv.transpose(), c[B])
    c_bar = c - np.dot(y, A)
    z_bar = sum(y * b)
    return A_prime, b_prime, c_bar, z_bar
