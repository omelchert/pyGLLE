import sys; sys.path.append('../scripts/')
import pyGLLE
from numpy import pi, sqrt, cosh

class SIM_SETUP:

    xMax = 20.
    Nx = 2**10
    P = 8.
    theta = 15.
    d3 = 0.0
    x0 = 0.0
    fName = 'stationary_solution.dat'

    def initial_field(self, x):
        Ax_fnc = lambda x: sqrt(2*self.theta)/cosh(sqrt(self.theta)*x)
        cosZeta = sqrt(8*self.theta)/self.P/pi
        sinZeta = sqrt(1-cosZeta*cosZeta)
        return Ax_fnc(x-self.x0)*(cosZeta+1j*sinZeta)

pyGLLE.findStationarySolution(SIM_SETUP())
