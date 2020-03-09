from numpy import asarray
from scipy.integrate import complex_ode


def solve(x, t, A0, fvec, callbackFunc):

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


