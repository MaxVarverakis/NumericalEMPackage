import EM as EMPackage
import numpy as np


# Problem 3.1
# em = EMPackage.EM3D(res = 1.)
direction = [1, 0, 0] # x-hat direction
# W = [(10, direction, (0, y, 0)) for y in np.linspace(-100, 100, 100)]
# Bx, By, Bz = em.B_tot(W)
# em.plotPlane((Bx, By, Bz), locQ = [(direction[0], *point) for point in [W[i][-1] for i in range(len(W))]], plane='yz', title=r'$\vec{K} = \hat{x}$')


# Problem 3.2
em = EMPackage.EM3D(res = .5)
center= (0,0,0)
r = 4
npts = 100
circle = [(center[0], center[1] + r * np.cos(2 * np.pi * i / npts), center[2] + r * np.sin(2 * np.pi * i / npts)) for i in range(npts)]
W = [(1, direction, point) for point in circle]
Bx, By, Bz = em.B_tot(W)
em.plotPlane((Bx, By, Bz), locQ = [(direction[0], *point) for point in circle], plane='yz', title=r'$\vec{K} = \hat{x}$')