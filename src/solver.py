"""solver.py

Contains function implementing a numerical integration scheme using the
complex_ode class of scipys integrate module.

AUTHOR: O. Melchert
DATE: 2020-01-17
"""
from numpy import asarray
from scipy.integrate import complex_ode


def solve(x, t, A0, fvec, callbackFunc):
    """ solve

    implements numerical integration scheme for complex field based on the
    explicit higher-order Runge-Kutta method "DOP853" (hard-coded).

    Args:
        x (numpy-array): discrete x-domain
        t (numpy-array): discrete t-domain
        A0 (numpy-array): initial condition
        fvec (object): right-hand-side of first order propagation equation
        callbaclFunc (object): callback function facilitating the measurement
            at distinct values of t. It takes 4 paramters in the form
            callbackFunc(n, tCurr, x, Ax), where:

            n (int): current propagation step
            t_curr (float): current time coordinate
            x (numpy-array): discrete x-domain
            Ax (numpy-array): field configuration at t_curr

    Returns: (t_fin,A_fin)
        t_fin (float): final time coordinate
        A_fin (numpy-array): final field configuration
    """

    dt = t[1]-t[0]
    it = 0

    solver = complex_ode(lambda t, A: fvec(A))
    solver.set_integrator('dop853')
    solver.set_initial_value(A0, t.min())

    while solver.successful() and solver.t < t.max():
        solver.integrate(solver.t+dt,step=1)
        callbackFunc(it, solver.t, x, solver.y)
        it += 1

    return solver.t, solver.y

# EOF: solver.py
