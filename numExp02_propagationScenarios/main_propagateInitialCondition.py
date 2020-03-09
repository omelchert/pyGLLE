import sys; sys.path.append('../scripts/')
import pyGLLE
import numpy as np



class SIM_SETUP:

    _inFileName = './data_stationary_solution/stationary_solution.dat.npz'
    _data = np.load(_inFileName)
    _x    = _data['x']
    _Ax0  = _data['Ax0']
    xMax  = float(_data['xMax'])
    Nx    = int(_data['Nx'])
    P     = float(_data['P'])
    theta = float(_data['theta'])
    x0    = float(_data['x0'])

    tMax = 6.0
    Nt = 10000
    nSkip = 20
    d2 = -1.00
    d3 = float(sys.argv[1])
    d4 = float(sys.argv[2])

    fName = 'GLLE_nCS1_xMax%lf_Nx%d_tMax%lf_Nt%d_P%lf_theta%lf_d2%lf_d3%lf_d4%lf_x0%lf.dat'%(xMax,Nx,tMax,Nt,P,theta,d2,d3,d4,x0)

    def initial_field(self, x):
        return self._Ax0


pyGLLE.propagateInitialCondition(SIM_SETUP())
