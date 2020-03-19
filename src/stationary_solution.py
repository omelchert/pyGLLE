"""stationary_solution.py

Contains function definitions allowing to obtain a homogeneous stationary
solution, possibly including one or several localized dissipatice structures,
for the standard Lugiato-Lefever equation.

AUTHOR: O. Melchert
DATE: 2020-01-17
"""
import sys
import numpy as np
import scipy.fftpack as sfft
from scipy.optimize import root


def stationarySolution_homogeneous(theta,P):
    """determine homogeneous stationary solution

    Args:
       theta (float): detuning
       P (float): amplitude of homogeneous driving field

    Returns:
       reA0 (float): real part of homogeneous stationary solution
       imA0 (float): imaginary part of homogeneous stationary solution
    """
    I0_ini = np.abs(1j*P/(theta + 1j))
    I0_opt = float(root( lambda I0: I0*(1+(theta-I0)**2) - P**2, I0_ini , tol=1e-8).x)
    reA0 = P/(1.+(I0_opt-theta)**2)
    imA0 = (I0_opt-theta)*P/(1.+(I0_opt-theta)**2)
    return reA0, imA0

def stationarySolution(x, A_ini, LLE_rhs, tol):
    """determine stationary solution for standard Lugiato-Lefever equation

    uses newton-krylov method (hardcoded) to perform root-finding
    procedure for standard Lugiato-Lefever equation (LLE)

    Args:
       x (numpy-array): discretized x-domain
       A_ini (numpy-array): trial solution used for root-finding procedure
       LLE_rhs (object): right-hand side of LLE
       tol (float): tolerance value used to terminate root-finding procedure

    Returns:
       A_opt (numpy-array): field resulting from root-finding procedure
    """
    k = sfft.fftfreq(x.size,d=x[1]-x[0])*2*np.pi

    def fvec(A):
        f = LLE_rhs(A)
        #sys.stderr.write("sum(abs(A)) = %lf\n"%(np.sum(np.abs(f))))
        return f

    A_opt = root(
            lambda A_r: (LLE_rhs(A_r.view(np.complex128))).view(np.float64),
            #lambda A_r: (fvec(A_r.view(np.complex128))).view(np.float64),
            np.array(A_ini, dtype=np.complex128).view(np.float64),
            method='krylov',
            tol=tol
            ).x.view(np.complex128)

    return A_opt

# EOF: stationary_solution.py 
