import EM as EMPackage
import numpy as np

em = EMPackage.EM3D(res = .25, lims = (-5, 6))

direction = [0, 0, 1] # z-hat direction
center= (0,0,0) # origin
a = 1
b = 2
npts = 100

def ring(num_points, a, b):
    # oriented along z axis
    points = [(0,0,(0,0,0)) for i in range(num_points)]
    for i in range(num_points):
        phi = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(a**2, b**2))  # Ensure uniform distribution on the surfaces

        x = r * np.cos(phi)
        y = r * np.sin(phi)
        z = 0

        points[i] = ((1/r, direction, (x, y, z)))

    return points

W = ring(npts, a, b)
Bx, By, Bz = em.B_tot(W)
em.plotPlane((Bx, By, Bz), locQ = [(direction[2], *point) for point in [W[i][-1] for i in range(len(W))]], plane='xy', title=f'a = {a}, b = {b}')