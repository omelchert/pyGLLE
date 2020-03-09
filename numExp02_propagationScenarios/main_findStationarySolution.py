import sys; sys.path.append('../scripts/')
import pyGLLE
import numpy as np


class SIM_SETUP:

    xMax = 160.
    Nx = 2**13
    P = 8.
    theta = 15.
    d2 = -1.0
    d3 = 0.0
    d4 = 0.0
    x0 = 0.0

    fName = 'stationary_solution.dat'

    def initial_field(self, x):
        Ax_fnc = lambda x: np.sqrt(2*self.theta)/np.cosh(x*np.sqrt(self.theta))
        cosZeta = np.sqrt(8*self.theta)/self.P/np.pi
        sinZeta = np.sqrt(1-cosZeta*cosZeta)
        return Ax_fnc(x-self.x0)*(cosZeta+1j*sinZeta)


pyGLLE.findStationarySolution(SIM_SETUP())
