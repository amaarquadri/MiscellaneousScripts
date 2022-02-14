import numpy as np
import matplotlib.pyplot as plt


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)

    def __mul__(self, scalar):
        return Vector(scalar * self.x, scalar * self.y)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)


def bezier(points, t):
    if len(points) == 1:
        return points[0]
    start = bezier(points[:-1], t)
    end = bezier(points[1:], t)
    return start + t * (end - start)


def plot(points, resolution=0.01):
    points_x = [vec.x for vec in points]
    points_y = [vec.y for vec in points]
    curve_x = []
    curve_y = []
    for t in np.arange(0, 1, step=resolution):
        vec = bezier(points, t)
        curve_x.append(vec.x)
        curve_y.append(vec.y)
    plt.plot(curve_x, curve_y, c='blue')
    plt.scatter(points_x, points_y, c='red')
    plt.show()


if __name__ == '__main__':
    plot([Vector(0, 0), Vector(1, 2), Vector(3, -2), Vector(6, 0), Vector(10, 3)])
