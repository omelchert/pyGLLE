""" pyGLLE.py

AUTHOR: O. Melchert
DATE: 2020-01-17
"""
import sys; sys.path.append('../src/')
import os
import datetime
import numpy as np
import scipy.fftpack as sfft
from stationary_solution import stationarySolution, stationarySolution_homogeneous
from data_handler import DataHandler
from solver import solve

__version__='1.0'


def findStationarySolution(setup, tol=1e-8):

    # -- INITIALIZE COMPUTATIONAL DOMAIN
    x = np.linspace(-setup.xMax, setup.xMax, setup.Nx, endpoint=False)
    k = sfft.fftfreq(x.size,d=x[1]-x[0])*2*np.pi

    # -- RIGHT HAND SIDE GENERATOR FOR GENERALIZED LUGIATO-LEFEVER PDE
    def _LLE_rhs(P, theta):
        return lambda A: P -(1+1j*theta)*A + sfft.fft((-1j*k*k)*sfft.ifft(A)) + 1j*np.abs(A)**2*A

    # -- ANSATZ FOR LOCALIZED SOLUTION
    Ax0_loc = setup.initial_field(x)

    # -- DETERMINE HOMOGENEOUS STATIONARY SOLUTION
    reA0, imA0 = stationarySolution_homogeneous(setup.theta,setup.P)

    # -- COMPOSE INITIAL GUESS FOR STATIONARY SOLUTION
    Ax0_ini = Ax0_loc + (reA0+1j*imA0)

    # -- DETERMINE STATIONARY SOLUTION FOR STANDART LLE (D3=0) USING INITIAL GUESS 
    A_statSol = stationarySolution(x, Ax0_ini, _LLE_rhs(setup.P, setup.theta), tol)

    # -- SAVE DATA
    path = './data_stationary_solution/'
    try:
        os.makedirs(path)
    except OSError:
        pass
    np.savez_compressed(path+setup.fName, x = np.asarray(x), Ax0 = np.asarray(A_statSol), P = setup.P, theta=setup.theta, d3=setup.d3, x0=setup.x0, Nx = setup.Nx, xMax=setup.xMax, Ax0_ini=np.asarray(Ax0_ini))


def propagateInitialCondition(setup):

    # -- CATCH POSSIBLE VALUE ERRORS FROM SETUP SUPPLIED PARAMETERS 
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
    info["I02 OS-ENV"]  = "%s"%(str(os.uname()))
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
