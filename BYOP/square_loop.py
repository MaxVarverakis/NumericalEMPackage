import numpy as np
import matplotlib.pyplot as plt

lims = (-6, 6)
a = 4
x = np.linspace(*lims, 200)

plt.plot(x, x / np.sinh(x))
# plt.vlines([-a, a], -a, a, linestyles='dashed', color='k')
# plt.hlines([-a, a], -a, a, linestyles='dashed', color='k')
# plt.xlim(lims)
# plt.ylim(lims)
plt.xlabel(r'$z$')
plt.ylabel(r'$B(z)$')
plt.show()