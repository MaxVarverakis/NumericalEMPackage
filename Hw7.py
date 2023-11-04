import scipy.constants as constants
import EM as EMPackage
import numpy as np
import matplotlib.pyplot as plt


# Griffiths Example 4.5
center = (0,0)
a = 4
b = 6.5
npts = 75

# NOTE: Bound volume charge is zero.
# Take other constants in sigma_b equal to 1 for simplicity!
em = EMPackage.EM2D(res = .25)
Q1 = [(-constants.e / a**2, center[0] + a * np.cos(2 * np.pi * i / npts), center[1] + a * np.sin(2 * np.pi * i / npts)) for i in range(npts)]
Q2 = [(constants.e / b**2, center[0] + b * np.cos(2 * np.pi * i / npts), center[1] + b * np.sin(2 * np.pi * i / npts)) for i in range(npts)]
Q = np.vstack((Q1, Q2, [(npts*constants.e, 0, 0)]))

Ex, Ey = em.E(Q, max_len=5e-9)
em.plotPlane((Ex, Ey), plane='yz', locQ = Q, title=f'Dielectric Shell: a = {a}, b = {b}')

# Dielectric --> Conductor ==> surface charges are exactly opposite
Q1 = [(-constants.e, center[0] + a * np.cos(2 * np.pi * i / npts), center[1] + a * np.sin(2 * np.pi * i / npts)) for i in range(npts)]
Q2 = [(constants.e, center[0] + b * np.cos(2 * np.pi * i / npts), center[1] + b * np.sin(2 * np.pi * i / npts)) for i in range(npts)]
Q = np.vstack((Q1, Q2, [(npts*constants.e, 0, 0)]))

Ex, Ey = em.E(Q, max_len=5e-9)
em.plotPlane((Ex, Ey), plane='yz', locQ = Q, title=f'Conducting Shell: a = {a}, b = {b}')

############################################################################################################
# Problem 3
em = EMPackage.EM3D(res = 1.)

a = 4
direction1 = [1, 0, 0]
point1 = (0, -a, 0)
Bx1, By1, Bz1 = em.B_infinite_wire(direction1, point1)
em.plotPlane((Bx1, By1, Bz1), locQ = [(direction1[0], *point1)], plane='yz', title=f'One Wire: a = {a}')

direction2 = [-1, 0, 0]
point2 = (0, a, 0)
Bx2, By2, Bz2 = em.B_infinite_wire(direction2, point2)
em.plotPlane((Bx1 + Bx2, By1 + By2, Bz1 + Bz2), locQ = [(direction1[0], *point1), (direction2[0], *point2)], plane='yz', title=f'Two Wires: a = {a}')
