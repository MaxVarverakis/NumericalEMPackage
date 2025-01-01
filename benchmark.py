import EM as EMPackage
import numpy as np
import matplotlib.pyplot as plt
import time

nump = [11, 101, 201, 501, 1001]
time_to_run = np.zeros_like(nump)

for idx,numPoints in enumerate(nump):
    print(f'Starting run #{idx+1}...')
    st = time.time()
    lims = (-5,5)
    em = EMPackage.EM2D(lims=lims, res=10/numPoints)
    Q = [(-1,0,0)]
    Ex, Ey = em.E(Q)

    et = time.time()
    time_to_run[idx] = et-st
    print(et-st)

print(time_to_run)



# magnitude = np.sqrt(Ex**2 + Ey**2)
# Ex /= magnitude
# Ey /= magnitude

# clim = 5e9
# numShow = 2
# plt.quiver(em.X[::numShow], em.Y[::numShow], Ex[::numShow], Ey[::numShow], magnitude[::numShow], cmap='RdBu_r', clim=(-clim,clim))
# plt.xlim(lims)
# plt.ylim(lims)
# plt.show()
