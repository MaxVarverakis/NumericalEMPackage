import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constants

# NEED TO IMPLEMENT SOLVING ONLY IN PLANE OF INTEREST OPTION

class EM3D():
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
    
    def E(self, charge_distribution, max_len = np.inf):
        Ex, Ey, Ez = np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0])), np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0])), np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0]))
        for q,x,y,z in charge_distribution:
            rSource = np.array([x, y, z])
            r = self.R - rSource
            for i in range(self.X.shape[0]):
                for j in range(self.Y.shape[0]):
                    for k in range(self.Z.shape[0]):
                        rMag = np.linalg.norm(r[i, j, k])
                        if rMag > 0.:
                            rHat = r[i, j, k] / rMag
                            dE = self.k * q * rHat / rMag**2
                            Ex[i, j, k] += dE[0]
                            Ey[i, j, k] += dE[1]
                            Ez[i, j, k] += dE[2]

        self.arrowFitler((Ex, Ey, Ez), max_len)
        return Ex, Ey, Ez

    def B_infinite_wire(self, direction: list, point: tuple, I = 1, wire_reference_points = 1, max_len = np.inf):
        '''
        Parameters
        ----------
        direction : list
            Direction of the wire (e.g., [1, 0, 0] for x-direction). This is like dl in the formula in Griffiths Eqn. 5.34
        point : tuple
            Point on the wire.
        I : float (optional)
            Current in the wire. Defaults to 1.
        wire_reference_points : int
            Number of points along the wire to use in the calculation. Defaults to 1 (use 1 if looking at field perpendicular to wire direction).
        '''
        Bx = np.zeros(self.X.shape)
        By = np.zeros(self.Y.shape)
        Bz = np.zeros(self.Z.shape)
        direction /= np.linalg.norm(direction) # normalize direction vector

        # phi_hat = np.array([-direction[1], direction[0], 0])
        # phi_hat /= np.linalg.norm(phi_hat)

        if wire_reference_points == 1:
            wire_ref = [point]
        else:
            step_size = abs(self.lims[1] - self.lims[0]) / (wire_reference_points - 1)
            wire_ref = [point + i * direction * step_size for i in range(-wire_reference_points, wire_reference_points + 1)]
        
        for rSource in wire_ref:
            r = self.R - rSource
            for i in range(self.X.shape[0]):
                for j in range(self.Y.shape[1]):
                    for k in range(self.Z.shape[2]):
                        rMag = np.linalg.norm(r[i, j, k])
                        if rMag > 0.:
                            rHat = r[i, j, k] / rMag
                            dB = (I / rMag**2) * np.cross(direction, rHat)
                            Bx[i, j, k] += dB[0]
                            By[i, j, k] += dB[1]
                            Bz[i, j, k] += dB[2]

        self.arrowFitler((Bx, By, Bz), max_len)
        return Bx, By, Bz

    def B_tot(self, wire_distribution: list, wire_reference_points = 100, max_len = np.inf):
        Bx = np.zeros(self.X.shape)
        By = np.zeros(self.Y.shape)
        Bz = np.zeros(self.Z.shape)

        for I, direction, point in wire_distribution:
            Bx1, By1, Bz1 = self.B_infinite_wire(direction, point, I, wire_reference_points)
            Bx += Bx1
            By += By1
            Bz += Bz1

        self.arrowFitler((Bx, By, Bz), max_len)
        return Bx, By, Bz

    def V(self, charge_distribution):
        V = np.zeros((self.X.shape[0], self.Y.shape[0], self.Z.shape[0]))
        for q,x,y,z in charge_distribution:
            rSource = np.array([x, y, z])
            r = self.R - rSource
            for i in range(self.X.shape[0]):
                for j in range(self.Y.shape[0]):
                    for k in range(self.Z.shape[0]):
                        rMag = np.linalg.norm(r[i, j, k])
                        if rMag > 0.:
                            V[i, j, k] += self.k * q / rMag

        return V

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

    def plotV(self, F, plane: str, locQ = None, slice: int = 0, title = '', pt_size = 5, cmap = 'RdBu', vmin = None, vmax = None, show = True):
        if -1 <= slice <= 1:
            idx = int((slice + 1) * (self.X.shape[0] - 1) / 2)
        else:
            raise ValueError("Slice must be a float between -1 and 1.")
        
        cDict = {-1: 'b', 0: 'k', 1: 'r'}

        if plane == 'xy':
            plt.pclormesh(self.X[:, :, idx], self.Y[:, :, idx], F[:, :, idx], cmap = cmap, vmin = vmin, vmax = vmax)
            if locQ is not None:
                plt.scatter([q[1] for q in locQ], [q[2] for q in locQ], color=[cDict[np.sign(q[0])] for q in locQ], s=pt_size)
        elif plane == 'xz':
            plt.pcolormesh(self.X[idx, :, :], self.Z[idx, :, :], F[idx, :, :], cmap = cmap, vmin = vmin, vmax = vmax)
            if locQ is not None:
                plt.scatter([q[1] for q in locQ], [q[3] for q in locQ], color=[cDict[np.sign(q[0])] for q in locQ], s=pt_size)
        elif plane == 'yz':
            plt.pcolormesh(self.Y[:, idx, :], self.Z[:, idx, :], F[:, idx, :], cmap = cmap, vmin = vmin, vmax = vmax)
            if locQ is not None:
                plt.scatter([q[2] for q in locQ], [q[3] for q in locQ], color=[cDict[np.sign(q[0])] for q in locQ], s=pt_size)
        else:
            raise ValueError("Plane must be one of 'xy', 'xz', or 'yz'.")
        
        cb = plt.colorbar()
        cb.formatter.set_useMathText(True)
        cb.formatter.set_powerlimits((0, 0))
        cb.set_label(r'$V(\vec{r})$', fontsize = 18)
        plt.xlabel(plane[0])
        plt.ylabel(plane[1])
        plt.title(title)
        plt.xlim(self.lims[0], self.lims[1] - 1)
        plt.ylim(self.lims[0], self.lims[1] - 1)
        plt.gca().set_aspect('equal', adjustable='box')
        if show:
            plt.show()

    def plotPlane(self, F: tuple, plane: str, locQ = None, slice: int = 0, title = '', pt_size = 5, show = True):
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
        
        cDict = {-1: 'b', 0: 'k', 1: 'r'}

        if plane == 'xy':
            plt.quiver(self.X[:, :, idx], self.Y[:, :, idx], F[0][:, :, idx], F[1][:, :, idx])
            if locQ is not None:
                plt.scatter([q[1] for q in locQ], [q[2] for q in locQ], color=[cDict[np.sign(q[0])] for q in locQ], s=pt_size)
        elif plane == 'xz':
            plt.quiver(self.X[idx, :, :], self.Z[idx, :, :], F[0][idx, :, :], F[2][idx, :, :])
            if locQ is not None:
                plt.scatter([q[1] for q in locQ], [q[3] for q in locQ], color=[cDict[np.sign(q[0])] for q in locQ], s=pt_size)
        elif plane == 'yz':
            plt.quiver(self.Y[:, idx, :], self.Z[:, idx, :], F[1][:, idx, :], F[2][:, idx, :])
            if locQ is not None:
                plt.scatter([q[2] for q in locQ], [q[3] for q in locQ], color=[cDict[np.sign(q[0])] for q in locQ], s=pt_size)
        else:
            raise ValueError("Plane must be one of 'xy', 'xz', or 'yz'.")

        plt.xlabel(plane[0])
        plt.ylabel(plane[1])
        plt.title(title)
        plt.xlim(self.lims[0], self.lims[1] - 1)
        plt.ylim(self.lims[0], self.lims[1] - 1)
        plt.gca().set_aspect('equal', adjustable='box')
        if show:
            plt.show()

class EM2D():
    def __init__(self, lims = (-10, 11), res = 1) -> None:
        self.q_e = constants.e
        self.k = 1 / (4 * np.pi * constants.epsilon_0)
        
        self.lims = lims
        self.res = res
        self.X, self.Y= np.meshgrid(np.arange(*lims, res), np.arange(*lims, res))
        self.R = self.createR()

    def createR(self):
        R = np.zeros((self.X.shape[0], self.Y.shape[0], 2))
        for i in range(self.X.shape[0]):
            for j in range(self.Y.shape[0]):
                R[i, j, 0] = self.X[i, j]
                R[i, j, 1] = self.Y[i, j]

        return R
    
    def E(self, charge_distribution, max_len = np.inf):
        Ex, Ey = np.zeros((self.X.shape[0], self.Y.shape[0])), np.zeros((self.X.shape[0], self.Y.shape[0]))
        for q,x,y in charge_distribution:
            rSource = np.array([x, y])
            r = self.R - rSource
            for i in range(self.X.shape[0]):
                for j in range(self.Y.shape[0]):
                    rMag = np.linalg.norm(r[i, j])
                    if rMag > 0.:
                        rHat = r[i, j] / rMag
                        dE = self.k * q * rHat / rMag**2
                        Ex[i, j] += dE[0]
                        Ey[i, j] += dE[1]

        self.arrowFitler((Ex, Ey), max_len)
        return Ex, Ey

    def V(self, charge_distribution):
        V = np.zeros((self.X.shape[0], self.Y.shape[0]))
        for q,x,y in charge_distribution:
            rSource = np.array([x, y])
            r = self.R - rSource
            for i in range(self.X.shape[0]):
                for j in range(self.Y.shape[0]):
                    rMag = np.linalg.norm(r[i, j])
                    if rMag > 0.:
                        V[i, j] += self.k * q / rMag

        return V

    def B_infinite_wire(self, direction: list, point: tuple, I = 1, max_len = np.inf):
        '''
        Parameters
        ----------
        direction : list
            Direction of the wire (-1 for into the plane and +1 for out of the plane).
        point : tuple
            Point on the wire that intersects plane.
        I : float (optional)
            Current in the wire. Defaults to 1.
        '''
        Bx = np.zeros(self.X.shape)
        By = np.zeros(self.Y.shape)
        direction /= np.linalg.norm(direction) # normalize direction vector
        
        r = self.R - point
        for i in range(self.X.shape[0]):
            for j in range(self.Y.shape[1]):
                rMag = np.linalg.norm(r[i, j])
                if rMag > 0.:
                    rHat = r[i, j] / rMag
                    dB = (I / rMag**2) * np.cross([0, 0, direction], rHat)
                    Bx[i, j] += dB[0]
                    By[i, j] += dB[1]

        self.arrowFitler((Bx, By), max_len)
        return Bx, By

    def B_tot(self, wire_distribution: list, max_len = np.inf):
        Bx = np.zeros(self.X.shape)
        By = np.zeros(self.Y.shape)

        for I, direction, point in wire_distribution:
            Bx1, By1 = self.B_infinite_wire(direction, point, I)
            Bx += Bx1
            By += By1

        self.arrowFitler((Bx, By), max_len)
        return Bx, By

    def arrowFitler(self, F: tuple, max_len):
        Fx, Fy = F
        for i in range(Fx.shape[0]):
            for j in range(Fx.shape[1]):
                if np.linalg.norm([Fx[i, j], Fy[i, j]]) > max_len:
                    Fx[i, j] = 0
                    Fy[i, j] = 0

    def plotPlane(self, F: tuple, plane: str, locQ = None, title = '', pt_size = 5, show = True):
        '''
        Parameters
        ----------
        F : tuple 
            Tuple of field components (e.g., (Ex, Ey)).
        plane : str
            x- and y-axis labels. Common inputs are 'xy', 'xz', or 'yz'.
        locQ : list
            List of tuples of the form (q, x, y) where q is the charge magnitude and x,y are the coordinates. If provided, the charge locations will be plotted.
        '''
        
        cDict = {-1: 'b', 0: 'k', 1: 'r'}

        plt.quiver(self.X, self.Y, F[0], F[1])
        if locQ is not None:
            plt.scatter([q[1] for q in locQ], [q[2] for q in locQ], color=[cDict[np.sign(q[0])] for q in locQ], s=pt_size)

        plt.xlabel(plane[0])
        plt.ylabel(plane[1])
        plt.title(title)
        plt.xlim(self.lims[0], self.lims[1] - 1)
        plt.ylim(self.lims[0], self.lims[1] - 1)
        plt.gca().set_aspect('equal', adjustable='box')
        if show:
            plt.show()





