import EM as EMPackage
import numpy as np
import matplotlib.pyplot as plt

# em = EMPackage.EM2D(res = .5)

# npts = 300
# a = 3
# k1 = .1
# k2 = k1/a**2
# def fill_circle(num_points, k1, k2, a):
#     # oriented along z axis
#     points = [(0,0,(0,0)) for i in range(num_points)]
#     for i in range(num_points):
#         phi = np.random.uniform(0, 2 * np.pi)
#         r = np.sqrt(np.random.uniform(0, a**2))  # Ensure uniform distribution on the surfaces

#         x = r * np.cos(phi)
#         y = r * np.sin(phi)
        
#         if r == a:
#             I = k1
#             direction = 1 # z-hat direction
#         else:
#             I = k2 * r
#             direction = -1 # -z-hat direction
        
#         points[i] = (I, direction, (x, y))

#     return points

# W_fill = fill_circle(npts, k1, k2, a)

# scale = 5
# outer_circle = [(k1, 1, (a * np.cos(2 * np.pi * i / int(npts/scale)), a * np.sin(2 * np.pi * i / int(npts/scale)))) for i in range(int(npts/scale))]
# W = np.vstack((W_fill, outer_circle))

# points = [(point) for point in [W[i][-1] for i in range(len(W))]]
# locs = [(direction, *point) for direction, point in zip([W[i][1] for i in range(len(W))], points)]
# # dirs = [direction for direction in [W[i][1] for i in range(len(W))]]

# Bx, By = em.B_tot(W, max_len=1)
# em.plotPlane((Bx, By), locQ = locs, plane='xy', title=f' a = {a}, $k_1$ = {k1}, ' + r'$k_2 = \frac{k_1}{a^2}$')

#############################################################
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def f1(z, t):
    return np.exp(z - t)**2

def f2(z, t):
    return np.sin(z - t)

def f3(z, t):
    return 1 / ((z-t)**2 + 1)

def f4(z, t):
    return np.exp(z**2 + t)

def f5(z, t):
    return np.sin(z) * np.cos(t)**3

def f6(z, t):
    return np.exp(-z**2) * np.sin(t)

z = np.linspace(-5, 5, 100)
t = np.linspace(0, 10, 100)
Z, T = np.meshgrid(z, t)
fig = plt.figure()
ax = plt.axes(projection='3d')

# ax.plot_surface(Z, T, f6(Z, T))
# ax.set_xlabel(r'$z$')
# ax.set_ylabel(r'$t$')
# ax.set_zlabel(r'$f_6(z,t)$')
# ax.set_title(r'$f_6(z,t) = e^{-z^2} \sin(t)$')
# plt.show()

def E_B_Wave(z, t):
    return np.cos(z-t)

z = np.linspace(-np.pi/2, 5*np.pi/2, 100)

ax.plot(z, E_B_Wave(z, 0), zs = 0, zdir = 'z', color = 'tab:blue', label=r'$B$')
verts = [(z_i, 0, E_B_Wave(z_i, 0)) for z_i in z]
poly1 = Poly3DCollection([verts], color='tab:orange', alpha=0.5)
ax.add_collection3d(poly1)

ax.plot(z, E_B_Wave(z, 0), zs = 0, zdir = 'y', color = 'tab:orange', label=r'$E$')
verts = [(z_i, E_B_Wave(z_i, 0), 0) for z_i in z]
poly2 = Poly3DCollection([verts], color='tab:blue', alpha=0.5)
ax.add_collection3d(poly2)

ax.set_xlabel(r'$z$')
ax.set_zlabel(r'$x$')
ax.set_ylabel(r'$y$')
plt.legend()
plt.show()


#############################################################

# Debugging stuff!

# 3D
# em = EMPackage.EM3D(res = .5)
# a = 0
# direction1 = [1, 0, 0]
# point1 = (0, -a, 0)
# Bx1, By1, Bz1 = em.B_infinite_wire(direction1, point1, max_len=.25, wire_reference_points=1)
# em.plotPlane((Bx1, By1, Bz1), locQ = [(direction1[0], *point1)], plane='yz')

# 2D
# em = EMPackage.EM2D(res = .5)
# a = 0
# direction1 = -1
# point1 = (0, -a)
# Bx1, By1= em.B_infinite_wire(direction1, point1, max_len=.25)
# em.plotPlane((Bx1, By1), locQ = [(direction1, *point1)], plane='yz')