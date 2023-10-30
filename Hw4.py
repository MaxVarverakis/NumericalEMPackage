import numpy as np
import scipy.constants as constants
import EM as EMPackage
# import matplotlib.pyplot as plt

em = EMPackage.EM(res = .5)

# Griffiths 2.16
s = 4
L = 10 # half length
npts = 150

def cylinder(num_points, s, L, q, fill):
    # oriented along x axis
    points = np.zeros((num_points, 4))
    for i in range(num_points):
        phi = np.random.uniform(0, 2 * np.pi)
        if fill:
            r = np.sqrt(np.random.uniform(0, s**2))  # Ensure uniform distribution on the surface
        else:
            r = s

        x = np.random.uniform(-L, L)
        y = r * np.cos(phi)
        z = r * np.sin(phi)

        points[i] = (q, x, y, z)

    return points

def cylinder_2D(num_points, s, q, fill):
    # oriented along x axis
    points = np.zeros((num_points, 4))
    for i in range(num_points):
        phi = np.random.uniform(0, 2 * np.pi)
        if fill:
            r = np.sqrt(np.random.uniform(0, s**2))  # Ensure uniform distribution on the surface
        else:
            r = s

        x = 0
        y = r * np.cos(phi)
        z = r * np.sin(phi)

        points[i] = (q, x, y, z)

    return points

Q1 = cylinder_2D(npts, s, constants.e, fill = True)
Q2 = cylinder_2D(npts, 8, -constants.e, fill = False)
Q = np.append(Q1, Q2, axis=0)

# ax = plt.figure().add_subplot(projection='3d')
# # ax.quiver(em.X, em.Y, em.Z, Ex, Ey, Ez, length=2, normalize=True)
# ax.scatter(Q1[:, 1], Q1[:, 2], Q1[:, 3], color='red', s=2)
# ax.scatter(Q2[:, 1], Q2[:, 2], Q2[:, 3], color='blue', s=2)
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# ax.set_ylim(-10, 10)
# ax.set_xlim(-L, L)
# ax.set_zlim(-10, 10)
# plt.show()

# NOTE takes a long time to run with this many points
Ex, Ey, Ez = em.E(Q, max_len=1e-7)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title='Griffiths 2.16', pt_size=1)

# 3.1
center = (0, 0, 0)
num_points = int(2e2)
radius = 4
epsilon = -.25
Q = np.append([(constants.e, 0, epsilon, 0)], [(constants.e, center[0], center[1] + radius * np.cos(2 * np.pi * i / num_points), center[2] + radius * np.sin(2 * np.pi * i / num_points)) for i in range(num_points)], axis=0)
Ex, Ey, Ez = em.E(Q, max_len=1e-7)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title=f'Problem 3.1 \n Y-Perturbation: {epsilon:.2f}', pt_size=1)