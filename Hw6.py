import scipy.constants as constants
import EM as EMPackage

em = EMPackage.EM(res = .5)

d = 8
Q = [(constants.e, 0, 0, d/2), (-constants.e, 0, 0, -d/2)]
Ex, Ey, Ez = em.E(Q, max_len=5e-10)
em.plotPlane((Ex, Ey, Ez), plane='yz', locQ = Q, title=f'Charge Separation: {d:.2f}')