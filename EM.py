import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constants

class EM():
    def __init__(self, lims = (-10, 11), res = 1) -> None:
        self.q_e = constants.e
        self.k = 1 / (4 * np.pi * constants.epsilon_0)
        
        self.lims = lims
        self.res = res
        self.X, self.Y, self.Z = np.meshgrid(np.arange(*lims, res), np.arange(*lims, res), np.arange(*lims, res))
        self.R = self.createR()

    def createR(self):
        R = np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0], 3))
        for i in range(self.X.shape[0]):
            for j in range(self.Y.shape[0]):
                for k in range(self.Z.shape[0]):
                    R[i, j, k, 0] = self.X[i, j, k]
                    R[i, j, k, 1] = self.Y[i, j, k]
                    R[i, j, k, 2] = self.Z[i, j, k]
                # R[i, j, 0] = self.X[i, j]
                # R[i, j, 1] = self.Y[i, j]
                # R[i, j, 2] = self.Z[i, j]

        return R
    
    def E(self, Q, max_len = np.inf):
        Ex, Ey, Ez = np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0])), np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0])), np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0]))
        for q,x,y,z in Q:
            rSource = np.array([x, y, z])
            r = self.R - rSource
            for i in range(self.X.shape[0]):
                for j in range(self.Y.shape[0]):
                    for k in range(self.Z.shape[0]):
                        rMag = np.linalg.norm(r[i, j, k])
                        if rMag > 0.:
                            rHat = r[i, j, k] / rMag
                            E = self.k * q * rHat / rMag**2
                            Ex[i, j, k] += E[0]
                            Ey[i, j, k] += E[1]
                            Ez[i, j, k] += E[2]
                    # rMag = np.linalg.norm(r[i, j])
                    # rHat = r[i, j] / rMag
                    # E = self.k * q * rHat / rMag**2
                    # Ex[i, j] += E[0]
                    # Ey[i, j] += E[1]

        self.arrowFitler((Ex, Ey, Ez), max_len)
        return Ex, Ey, Ez

    def arrowFitler(self, F: tuple, max_len):
        Fx, Fy, Fz = F
        for i in range(Fx.shape[0]):
            for j in range(Fx.shape[1]):
                for k in range(Fx.shape[2]):
                    if np.linalg.norm([Fx[i, j, k], Fy[i, j, k], Fz[i, j, k]]) > max_len:
                        Fx[i, j, k] = 0
                        Fy[i, j, k] = 0
                        Fz[i, j, k] = 0
                # if np.linalg.norm([Fx[i, j], Fy[i, j]]) > max_len:
                #     Fx[i, j] = 0
                #     Fy[i, j] = 0

    def plotPlane(self, F: tuple, plane: str, locQ = None, slice: int = 0, title = '', pt_size = 5):
        '''
        Parameters
        ----------
        F : tuple 
            Tuple of field components (e.g., (Ex, Ey, Ez)).
        plane : str
            Plane to plot on. Must be one of 'xy', 'xz', or 'yz'.
        locQ : list
            List of tuples of the form (q, x, y, z) where q is the charge magnitude and x,y,z are the coordinates. If provided, the charge locations will be plotted.
        slice : float
            Normalized plane position within the range [-1, 1].
        '''
        if -1 <= slice <= 1:
            idx = int((slice + 1) * (self.X.shape[0] - 1) / 2)
        else:
            raise ValueError("Slice must be a float between -1 and 1.")
        
        if plane == 'xy':
            plt.quiver(self.X[:, :, idx], self.Y[:, :, idx], F[0][:, :, idx], F[1][:, :, idx])
            if locQ is not None:
                plt.scatter([q[1] for q in locQ], [q[2] for q in locQ], color='r', s=pt_size)
        elif plane == 'xz':
            plt.quiver(self.X[idx, :, :], self.Z[idx, :, :], F[0][idx, :, :], F[2][idx, :, :]) # xz plane
            if locQ is not None:
                plt.scatter([q[1] for q in locQ], [q[3] for q in locQ], color='r', s=pt_size)
        elif plane == 'yz':
            plt.quiver(self.Y[:, idx, :], self.Z[:, idx, :], F[1][:, idx, :], F[2][:, idx, :])
            if locQ is not None:
                plt.scatter([q[2] for q in locQ], [q[3] for q in locQ], color='r', s=pt_size)
        else:
            raise ValueError("Plane must be one of 'xy', 'xz', or 'yz'.")

        plt.xlabel(plane[0])
        plt.ylabel(plane[1])
        plt.title(title)
        plt.xlim(self.lims[0], self.lims[1] - 1)
        plt.ylim(self.lims[0], self.lims[1] - 1)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()





