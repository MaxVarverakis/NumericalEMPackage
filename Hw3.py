import numpy as np
import scipy.constants as constants
import EM as EMPackage

em = EMPackage.EM(res = .5)

# 3.1
L = 2
n = 2
pts = [
    [(constants.e, -L, y, 0) for y in np.arange(-L, L, 2**-n)],
    [(constants.e, L, y, 0) for y in np.arange(-L, L, 2**-n)],
    [(constants.e, x, -L, 0) for x in np.arange(-L, L, 2**-n)],
    [(constants.e, x, L, 0) for x in np.arange(-L, L, 2**-n)],
    [(constants.e, L, L, 0)]
]
Q = np.array([item for sublist in pts for item in sublist], dtype=tuple)

Ex, Ey, Ez = em.E(Q)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title='Problem 2.4')


# 3.2
center = (0, 0)
num_points = 50
radius = 3
Q = [(constants.e, center[0] + radius * np.cos(2 * np.pi * i / num_points), center[1] + radius * np.sin(2 * np.pi * i / num_points), 0) for i in range(num_points)]
Ex, Ey, Ez = em.E(Q, max_len=9e-9)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title='Problem 2.5')

# 3.3 TAKES LONG TIME TO RUN
L = 10
n = 0
Q = [(constants.e, x, y, 0) for x in np.arange(-L, L + 1, 2**-n) for y in np.arange(-L, L + 1, 2**-n)]
Ex, Ey, Ez = em.E(Q, max_len=9e-9)
em.plotPlane((Ex, Ey, Ez), plane='xz', locQ = Q, title='Example 2.5')

# 3.4
npts = 200
r = 3

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

        points.append((constants.e, x, y, z))

    return np.array(points)

Q = fibonacci_sphere(npts, r)

Ex, Ey, Ez = em.E(Q, max_len=9e-9)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title='Problem 2.11', pt_size=2.5)

# 3.5
def fill_sphere(sample, radius):
    points = []
    while len(points) < sample:
        u = np.random.uniform(0, 1)
        v = np.random.uniform(0, 1)
        theta = u * 2.0 * np.pi
        phi = np.arccos(2.0 * v - 1.0)
        r = radius * np.cbrt(np.random.uniform(0, 1))

        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        sin_phi = np.sin(phi)
        cos_phi = np.cos(phi)

        x = r * sin_phi * cos_theta
        y = r * sin_phi * sin_theta
        z = r * cos_phi

        points.append((constants.e, x, y, z))

    return np.array(points)

r = 9
npts = 500
Q = fill_sphere(npts, r)
Ex, Ey, Ez = em.E(Q, max_len=9e-9)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title='Problem 2.11', pt_size=2.5)

# 3.6
L = 25
Q = [(constants.e, 0, y, 0) for y in np.arange(-L, L + 1, 2**-4)]
Ex, Ey, Ez = em.E(Q, max_len=9e-9)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title='Problem 2.13', pt_size=1)



