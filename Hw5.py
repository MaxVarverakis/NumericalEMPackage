import numpy as np
import scipy.constants as constants
import EM as EMPackage
import matplotlib.pyplot as plt

# em = EMPackage.EM(res = .125)
em = EMPackage.EM(res = .25)

# Griffiths 3.7
d = 2
l = 5e-9
Q = [(-2*constants.e, 0, 0, d), (constants.e, 0, 0, 3*d), (2*constants.e, 0, 0, -d), (-constants.e, 0, 0, -3*d)]
# Ex, Ey, Ez = em.E(Q, max_len=4e-9)
# em.plotPlane((constants.e * Ex, constants.e * Ey, constants.e * Ez), plane='yz', locQ = Q, title='Problem 3.7', pt_size=2, show=False)
# V = em.V(Q)
# em.plotV(V, plane='yz', title='Problem 3.7', show=False, vmin = -l, vmax = l)
# plt.ylim(0,10)
# plt.gca().set_aspect('auto')
# plt.savefig('/Users/max/Library/CloudStorage/OneDrive-CalPoly/Quarters/F23/Phys 408/Hw5_3.7.png', dpi=300)
# plt.show()



# Problem 3
# Take k = 1 for simplicity!
def fibonacci_sphere(samples, radius):
    points = []
    phi = np.pi * (3. - np.sqrt(5.))  # Golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # Range from -1 to 1
        radius_at_height = np.sqrt(1 - y**2)  # Calculate radius at this height

        theta = phi * i  # Golden angle increment
        
        x = np.cos(theta) * radius_at_height
        z = np.sin(theta) * radius_at_height

        # Scale by the desired radius
        x *= radius
        y *= radius
        z *= radius

        points.append((constants.e * (z/radius), x, y, z))

    return np.array(points)

R = 2
npts = 50
l = 1e-8

Q = fibonacci_sphere(npts, R)
# cDict = {-1: 'b', 0: 'k', 1: 'r'}
# ax = plt.figure().add_subplot(projection='3d')
# ax.scatter(Q[:, 1], Q[:, 2], Q[:, 3], c=[(1e19 * q[0]) for q in Q], cmap = 'RdBu_r', s=2)
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# ax.set_ylim(-10, 10)
# ax.set_xlim(-10, 10)
# ax.set_zlim(-10, 10)
# plt.show()

V = em.V(Q)
em.plotV(V, plane='yz', title='Problem 3.7', show=False, vmin = -l, vmax = l)
plt.ylim(0,10)
plt.gca().set_aspect('auto')
plt.savefig('/Users/max/Library/CloudStorage/OneDrive-CalPoly/Quarters/F23/Phys 408/Hw5_P3_V.png', dpi=300)
plt.show()