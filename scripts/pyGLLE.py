""" pyGLLE.py

Main script implementing functions for determining stationary solutions to the
standard Lugiato-Lefever equation (LLE) and for propagating a user supplied
initial condtions in terms of the genaralized LLE.

AUTHOR: O. Melchert
DATE: 2020-01-17
"""
import sys #; sys.path.append('../src/')
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import datetime
import numpy as np
import scipy.fftpack as sfft
from stationary_solution import stationarySolution, stationarySolution_homogeneous
from data_handler import DataHandler
from solver import solve

__version__='1.0'


def findStationarySolution(setup, tol=1e-10):
    """determine stationary solution for standard LLE

    uses root-finding procedure to determine stationary solution to the
    standard Lugiato-Lefever equation

    Args:
        setup (object): interface class holding simulation paramters
        tol (float): tolerance for root-finding procedure  (default 1e-10)

    Returns: nothing, but saves result of root-finding procedure in folder
       ./data_stationary_solution/. The stored data consists of

        x (array): discrete x-mesh defining the computational domain
        Ax0_ini (array): trial solution
        Ax0 (array): result of root-finding procedure
        P (float): amplitude of homogeneous driving field
        theta (float): detuning
        Nx (int): number of mesh-points for discretizing x
        xMax (float): bound of x domain
    """

    # -- INITIALIZE COMPUTATIONAL DOMAIN
    x = np.linspace(-setup.xMax, setup.xMax, setup.Nx, endpoint=False)
    k = sfft.fftfreq(x.size,d=x[1]-x[0])*2*np.pi

    # -- RIGHT HAND SIDE GENERATOR FOR GENERALIZED LUGIATO-LEFEVER PDE
    def _LLE_rhs(P, theta):
        return lambda A: P -(1+1j*theta)*A + sfft.fft((-1j*k*k)*sfft.ifft(A)) + 1j*np.abs(A)**2*A

    # -- FETCH USER DEFINED TRIAL SOLUTION
    Ax0_loc = setup.initial_field(x)

    # -- DETERMINE HOMOGENEOUS STATIONARY SOLUTION
    reA0, imA0 = stationarySolution_homogeneous(setup.theta,setup.P)

    # -- COMPOSE INITIAL GUESS FOR STATIONARY SOLUTION
    Ax0_ini = Ax0_loc + (reA0+1j*imA0)

    # -- DETERMINE STATIONARY SOLUTION FOR STANDART LLE USING INITIAL GUESS
    A_statSol = stationarySolution(x, Ax0_ini, _LLE_rhs(setup.P, setup.theta), tol)

    # -- SAVE DATA
    path = './data_stationary_solution/'
    try:
        os.makedirs(path)
    except OSError:
        pass
    np.savez_compressed(path+setup.fName, x = np.asarray(x), Ax0 = np.asarray(A_statSol), P = setup.P, theta=setup.theta, d3=setup.d3, x0=setup.x0, Nx = setup.Nx, xMax=setup.xMax, Ax0_ini=np.asarray(Ax0_ini))


def propagateInitialCondition(setup):
    """propagate inital condition under the generalized Lugiato-Lefever equation

    uses pseudospectral approach to propagate a user supplied initial condition
    in terms of the generalized Lugiato-Lefever equation with third and fourth
    order dispersion.

    Args:
        setup (object): interface class holding simulation paramters

    Returns: nothing, but saves result in folder ./data/. The stored data
        consists of

        x (array): discrete x-mesh defining the computational domain
        t (array): discrete t-mesh defining t-coordinates at which data is stored
        Axt (array): field obtained during the simulation run
        info (str): metadata for data-management
    """

    # -- CATCH POSSIBLE DATATYPE ERRORS OF SUPPLIED PARAMETERS
    if not isinstance(setup.xMax, float):
        raise ValueError("xMax: expected float, got %s"%(type(setup.xMax)))

    if not isinstance(setup.Nx, int):
        raise ValueError("Nx: expected int, got %s"%(type(setup.Nx)))

    if not isinstance(setup.tMax, float):
        raise ValueError("tMax: expected float, got %s"%(type(setup.tMax)))

    if not isinstance(setup.Nt, int):
        raise ValueError("Nt: expected int, got %s"%(type(setup.Nt)))

    if not isinstance(setup.nSkip, int):
        raise ValueError("nSkip: expected int, got %s"%(type(setup.nSkip)))

    if not isinstance(setup.P, float):
        raise ValueError("P: expected float, got %s"%(type(setup.P)))

    if not isinstance(setup.theta, float):
        raise ValueError("theta: expected float, got %s"%(type(setup.theta)))

    if not isinstance(setup.d3, float):
        raise ValueError("d3: expected float, got %s"%(type(setup.d3)))

    if not isinstance(setup.d4, float):
        raise ValueError("d4: expected float, got %s"%(type(setup.d4)))

    if not isinstance(setup.fName, str):
        raise ValueError("fName: expected str, got %s"%(type(setup.fName)))

    # -- ASSEMBLE META-DATA
    info = dict()
    info["I01 OS-USER"] = "%s"%(os.path.expanduser('~'))
    info["I02 OS-ENV"]  = "%s"%(str(sys.platform))
    info["I03 OS-PID"]  = "%s"%(str(os.getpid()))
    info["I04 FILE"]    = "%s"%(sys.argv[0])
    info["I05 VERSION"] = "%s"%(__version__)
    info["I06 DATE"]    = "%s"%(datetime.datetime.now())
    info["I07 FNAME"]   = "%s"%(setup.fName)

    # -- INITIALIZE COMPUTATIONAL DOMAIN
    x = np.linspace(-setup.xMax, setup.xMax, setup.Nx, endpoint=False)
    k = sfft.fftfreq(x.size,d=x[1]-x[0])*2*np.pi
    t = np.linspace(0,setup.tMax,setup.Nt,endpoint=True)

    # -- RIGHT HAND SIDE GENERATOR FOR GENERALIZED LUGIATO-LEFEVER PDE
    def _GLLE_rhs(P, theta, d2, d3, d4):
        return lambda A: P -(1+1j*theta)*A + sfft.fft((1j*d2*k*k + 1j*d3*k*k*k + 1j*d4*k*k*k*k)*sfft.ifft(A)) + 1j*np.abs(A)**2*A

    # -- SET INITIAL CONDITION
    Ax0 = setup.initial_field(x)

    # -- PROPAGATE FIELD
    dat = DataHandler(setup.nSkip)
    solve(x, t, Ax0, _GLLE_rhs(setup.P, setup.theta, setup.d2, setup.d3, setup.d4), dat.measure)

    # -- SAVE DATA
    dat.save(setup.fName, path='./data/', **info)

# EOF: pyGLLE.py
