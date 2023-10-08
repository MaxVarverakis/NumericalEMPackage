import numpy as np
import matplotlib.pyplot as plt

def Va(x, y, z):
    return x**2, 3 * x * z**2, -2 * x * z

def Vb(x, y, z):
    return x * y, 2 * y * z, 3 * z * x

def Vc(x, y, z):
    return y**2, 2 * x * y + z**2, 2 * y * z

def yzPlot(V: np.ndarray, lims = [-10, 10], res = 1, title = ''):
    y,z = np.meshgrid(np.arange(lims[0], lims[1], res), np.arange(lims[0], lims[1], res))
    u,v = V(0, y, z)[1], V(0, y, z)[2]
    
    plt.quiver(y, z, u, v)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.title(title)
    plt.xlim(lims)
    plt.ylim(lims)
    plt.show()

if __name__ == '__main__':
    yzPlot(Va, title='Va')
    yzPlot(Vb, title='Vb')
    yzPlot(Vc, title='Vc')