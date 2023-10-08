import numpy as np
import scipy.constants as constants
import EM as EMPackage

em = EMPackage.EM(res = .5) # originally had res = 1 for the homework plots.

proj = 'xz'

# EXAMPLE 2.1
d = 5
z = 0
Q1 = [(constants.e, d/2, 1, z), (constants.e, -d/2, 1, -z)]
Ex, Ey, Ez = em.E(Q1, max_len=3e-10)
em.plotPlane((Ex, Ey, Ez), plane=proj, locQ = Q1, title=proj)

# em.xzPlot((Ex, Ey, Ez), locQ = Q1, slice = None, title='xz')
# em.xyPlot((Ex, Ey, Ez), locQ = Q1, slice = None, title='xy')
# em.yzPlot((Ex, Ey, Ez), locQ = Q1, slice = None, title='yz')

# ax = plt.figure().add_subplot(projection='3d')
# ax.quiver(em.X, em.Y, em.Z, Ex, Ey, Ez, length=2, normalize=True)
# ax.scatter([0], [0], [0], color='red', s=10)
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# plt.show()

# print("X shape:", em.X.shape)
# print("Z shape:", em.Z.shape)
# print("Ex shape:", Ex.shape)
# print("Ez shape:", Ez.shape)

# # Check if dimensions are compatible
# assert em.X.shape == Ex.shape
# assert em.Z.shape == Ez.shape

# PROBLEM 2.3
# L = 2.5
# Q2 = [(constants.e, x, 0, 0) for x in np.arange(-L, L + 1, 2**-4)]
# Ex, _, Ez = em.E(Q2)
# em.plotPlane((Ex, Ey, Ez), plane = proj, locQ = Q2, title='Problem 2')


# TEST
# center = (0, 0)
# num_points = int(1e2)
# radius = 3
# Q3 = [(constants.e, center[0] + radius * np.cos(2 * np.pi * i / num_points), center[1] + radius * np.sin(2 * np.pi * i / num_points)) for i in range(num_points)]
# Ex, Ez = em.E(Q3, max_len=9e-9)
# em.xzPlot((Ex, Ez), locQ = Q3, title='For Fun :)')