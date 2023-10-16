import numpy as np
import matplotlib.pyplot as plt

r = np.linspace(0, 1, 1000)
a = .1
b = .5

import numpy as np
import matplotlib.pyplot as plt

r = np.linspace(0, 1, 1000)
a = 0.1
b = 0.5

def E(r, a, b):
    result = np.zeros_like(r)
    mask1 = (r >= a) & (r < b)
    mask2 = r >= b
    
    result[mask1] = 1 / r[mask1]**2 * (np.sinh(r[mask1]) - np.sinh(a))
    result[mask2] = 1 / r[mask2]**2 * (np.sinh(b) - np.sinh(a))
    
    return result

plt.plot(r, E(r, a, b))
# plt.plot(r, 1e-2 * r**-2 * np.cosh(r))
plt.vlines(a, -.1, 3, linestyle='--', color='r', label='a')
plt.vlines(b, -.1, 3, linestyle='-.', color='k', label='b')
plt.legend()
plt.ylim(-.05, 3)
plt.xlim(0, 1)
plt.xlabel('r')
plt.ylabel('|E|')
# plt.savefig('/Users/max/Library/CloudStorage/OneDrive-CalPoly/Quarters/F23/Phys 408/BYOP/E_thick_shell.png', dpi=300)
plt.show()