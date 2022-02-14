import numpy as np
from scipy.spatial.transform import Rotation


def main():
    rot = Rotation.from_euler("XZ", np.array([45, 45]), degrees=True)
    print(rot.as_matrix())
    print(rot.as_euler("zxz", degrees=True))
    axis_angle = rot.as_rotvec(degrees=True)
    angle = np.linalg.norm(axis_angle)
    print(axis_angle / angle)
    print(angle)


if __name__ == '__main__':
    main()
