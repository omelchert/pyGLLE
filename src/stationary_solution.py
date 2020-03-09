import sys
import numpy as np
import scipy.fftpack as sfft
from scipy.optimize import root


def stationarySolution_homogeneous(theta,P):
    I0_ini = np.abs(1j*P/(theta + 1j))
    I0_opt = float(root( lambda I0: I0*(1+(theta-I0)**2) - P**2, I0_ini , tol=1e-8).x)
    reA0 = P/(1.+(I0_opt-theta)**2)
    imA0 = (I0_opt-theta)*P/(1.+(I0_opt-theta)**2)
    return reA0, imA0


def stationarySolution(x, A_ini, GLLE_rhs, tol):
    k = sfft.fftfreq(x.size,d=x[1]-x[0])*2*np.pi

    def fvec(A):
        f = GLLE_rhs(A)
        sys.stderr.write("sum(abs(A)) = %lf\n"%(np.sum(np.abs(f))))
        return f

    res = root(
            lambda A_r: (fvec(A_r.view(np.complex128))).view(np.float64),
            np.array(A_ini, dtype=np.complex128).view(np.float64),
            method='krylov',
            tol=tol
            ).x.view(np.complex128)

    return res


