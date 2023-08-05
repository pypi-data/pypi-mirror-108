"""
Functions related to obtaining the equilibrium starting conditions for ellipsoidal clouds with internal streaming.
"""
import numpy as np
import scipy.optimize as sco
from math import sqrt
from enum import IntEnum
import mpmath as mp

from src.solve.geometry import get_Ax, get_Az, get_Ay
from src.utils import EllipIndex, internal_streaming_axis_length_ratio_solver, get_ai_lengths
from src.solve.deriv_funcs import deriv_xdot_func, deriv_ydot_func, deriv_zdot_func


class VarIndex(IntEnum):
    """
    Enum to clean up vectorised derivative equations
    """
    x = 0
    y = 1
    z = 2


# Derivative equations for the ellipsoid in in vector form
def deriv_xdot_func_vec(vec_input, θ, θdot, ϕdot, A1, ρ_real_over_ρ_pressure, ρ_pressure_over_ρ_tides):
    """
    Compute the derivative of the derivative of the axis of the ellipsoid
    """
    return deriv_xdot_func(x=vec_input[VarIndex.x], y=vec_input[VarIndex.y], z=vec_input[VarIndex.z], A1=A1, θ=θ, θdot=θdot,
                           ϕdot=ϕdot, ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                           ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides)[0]


def deriv_ydot_func_vec(vec_input, θ, θdot, ϕdot, A2, ρ_real_over_ρ_pressure, ρ_pressure_over_ρ_tides):
    """
    Compute the derivative of the derivative of the axis of the ellipsoid ellipsoid
    """
    return deriv_ydot_func(x=vec_input[VarIndex.x], y=vec_input[VarIndex.y], z=vec_input[VarIndex.z], A2=A2, θ=θ, θdot=θdot,
                           ϕdot=ϕdot, ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                           ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides)[0]


def deriv_zdot_func_vec(vec_input, A3, ρ_real_over_ρ_pressure, ρ_pressure_over_ρ_tides):
    """
    Compute the derivative of the derivative of the axis of the ellipsoid
    """
    return deriv_zdot_func(x=vec_input[VarIndex.x], y=vec_input[VarIndex.y], z=vec_input[VarIndex.z], A3=A3,
                           ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                           ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides)[0]


def combined_deriv_eqs(x, ρ_real_over_ρ_pressure, ρ_pressure_over_ρ_tides, ϕdot):
    """
    List of vector form of derivative equations for scipy root
    """
    Ai = [
        get_Ax(x=x[VarIndex.x], y=x[VarIndex.y], z=x[VarIndex.z]),
        get_Ay(x=x[VarIndex.x], y=x[VarIndex.y], z=x[VarIndex.z]),
        get_Az(x=x[VarIndex.x], y=x[VarIndex.y], z=x[VarIndex.z])]

    return [
        deriv_xdot_func_vec(vec_input=x, θ=0, θdot=0, ϕdot=ϕdot, A1=Ai[EllipIndex.x],
                            ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                            ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides),
        deriv_ydot_func_vec(vec_input=x, θ=0, θdot=0, ϕdot=ϕdot, A2=Ai[EllipIndex.y],
                            ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                            ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides),
        deriv_zdot_func_vec(vec_input=x, A3=Ai[EllipIndex.z],
                            ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                            ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides)
    ]


def combined_deriv_eqs_quad(x, ρ_real_over_ρ_pressure, ρ_pressure_over_ρ_tides, ϕdot):
    """
    Vector form of derivative equations for scipy minimise to minimise the equations in quadrature.
    """
    Ai = [
        get_Ax(x=x[VarIndex.x], y=x[VarIndex.y], z=x[VarIndex.z]),
        get_Ay(x=x[VarIndex.x], y=x[VarIndex.y], z=x[VarIndex.z]),
        get_Az(x=x[VarIndex.x], y=x[VarIndex.y], z=x[VarIndex.z])]
    return deriv_xdot_func_vec(vec_input=x, θ=0, θdot=0, ϕdot=ϕdot, A1=Ai[EllipIndex.x],
                                ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                                ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides)**2 + \
            deriv_ydot_func_vec(vec_input=x, θ=0, θdot=0, ϕdot=ϕdot, A2=Ai[EllipIndex.y],
                                ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                                ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides)**2 + \
            deriv_zdot_func_vec(vec_input=x, A3=Ai[EllipIndex.z],
                                ρ_real_over_ρ_pressure=ρ_real_over_ρ_pressure,
                                ρ_pressure_over_ρ_tides=ρ_pressure_over_ρ_tides)**2


def get_rot_equ_axis_lengths(alpha, rho_lim, ρ_tides, ρ_init=1.0001, small_equ_set=True, final_only=True):
    """
    Calculates the equilibrium axis lengths based on the full ODE system for a ellipsoid with a given density, tidal
    density and with an internal streaming velocity. Initial conditions are initially calculated with no gravity.
    Following this the equilibrium solution to solved by "hopping" to the desired ellipsoidal conditions through solving
    the full ODE system with small increments in its parameters.
    :param alpha: int: internal streaming rate
    :param rho_lim: int: the maximum density value to be calculated. This should be between 1 and 4.
    :param ρ_tides: int: The tidal density
    :param ρ_init: int: The initial density of the cloud - does not need to be changed
    :param small_equ_set: bool: determine to use the larger or the smaller (unstable/stable) equ solutions.
    :param final_only: bool: return only the final (rho_lim) values for axis lengths
    :return:
    """

    if alpha == 0:
        raise SystemExit("Alpha was zero, select a non-zero value and rerun. Exiting. ")

    # Constants
    ϕdot = alpha * sqrt(ρ_tides)
    # Get the axis ratios and the lengths for the first step in which no gravity is considered to be acting.
    a2oa1, a3oa1 = internal_streaming_axis_length_ratio_solver(alpha)
    a1 = get_ai_lengths(alpha=alpha, ρ=ρ_init, ρ_tidal=ρ_tides, return_only_a1=True)
    a2 = a2oa1 * a1
    a3 = a3oa1 * a1
    no_grav_a1 = a1

    # Prepare the parameters to solve the ODE system.
    indexs_calculated = 0
    ai_list = []
    ρ_list = []
    flag_list = []
    # and solve for the first actual length of a1 WHERE GRAVITY IS INCLUDED.
    a1_new = sco.root(fun=combined_deriv_eqs, x0=np.array([a1, a2, a3]),
                      args=(ρ_init, 1/ρ_tides, ϕdot), method='anderson',
                      options={"maxiter": 1000, "fatol": 1e-13})
    # append the values to lists
    ai_list.append(a1_new.x)
    ρ_list.append(ρ_init)
    flag_list.append(a1_new.success)
    indexs_calculated += 1

    # Begin solving the system to the desired parameters.
    while True:
        a1_new = sco.root(fun=combined_deriv_eqs, x0=a1_new.x, args=(ρ_init, 1/ρ_tides, ϕdot),
                          method='lm',
                          options={"xtol": 1e-12, "maxfev": 100000, "ftol": 1e-5, "maxiter": 25000})
        # a1_new = sco.minimize(fun=combined_deriv_eqs_quad, x0=a1_new.x, args=(ρ_init, 1/ρ_tides, ϕdot), tol=1e-12, method="Nelder-Mead", options={"adaptive":True, "xatol": 1e-12, "maxfev": 100000, "fatol":1e-12})
        # a1_new = sco.differential_evolution(func=combined_deriv_eqs_quad, bounds=[(0.2, 1), (0.2, 1), (0.2, 1)], args=(ρ_init, 1/ρ_tides, ϕdot), tol=1e-12)
        indexs_calculated += 1
        ai_list.append(a1_new.x)
        ρ_list.append(ρ_init)
        flag_list.append(a1_new.success)

        if ρ_init > rho_lim:
            print("All values to limit were calculated")
            break

        # required for large equ set.
        prev_a1 = ai_list[-1][VarIndex.x]
        prev_a2 = ai_list[-1][VarIndex.y]
        prev_a3 = ai_list[-1][VarIndex.z]

        if small_equ_set:
            # If the solver found a negative root we invert it for the next step. NOTE. The negative values are saved
            # for plotting. They are not discarded and the absolute value taken.
            if a1_new.x[VarIndex.x] < 0:
                a1_new.x[VarIndex.x] = - a1_new.x[VarIndex.x]
            if a1_new.x[VarIndex.y] < 0:
                a1_new.x[VarIndex.y] = - a1_new.x[VarIndex.y]
            if a1_new.x[VarIndex.z] < 0:
                a1_new.x[VarIndex.z] = - a1_new.x[VarIndex.z]

            # Currently we look for solutions with lengths less than 5 - This is tides 0.001. Hence we reset the value
            if a1_new.x[VarIndex.x] > 5:
                a1_new.x[VarIndex.x] = 0.7
            if a1_new.x[VarIndex.y] > 1:
                a1_new.x[VarIndex.y] = 0.2
            if a1_new.x[VarIndex.z] > 5:
                a1_new.x[VarIndex.z] = 0.7

        elif not small_equ_set:
            # In this case if the axis lengths jump to negative values assign them the previous value.
            if a1_new.x[VarIndex.x] <= 0:
                a1_new.x[VarIndex.x] = prev_a1
            if a1_new.x[VarIndex.y] <= 0:
                a1_new.x[VarIndex.y] = prev_a2
            if a1_new.x[VarIndex.z] <= 0:
                a1_new.x[VarIndex.z] = prev_a3
            # In the case that the solver didn't find a new value we will increase the length by a bit, read 1 unit,
            # for the next guess.
            if prev_a1 == a1_new.x[VarIndex.x]:
                a1_new.x[VarIndex.x] = prev_a1 + 1
            if prev_a2 == a1_new.x[VarIndex.y]:
                a1_new.x[VarIndex.y] = prev_a1 + 1
            if prev_a3 == a1_new.x[VarIndex.z]:
                a1_new.x[VarIndex.z] = prev_a1 + 1

        else:
            print("Did not select which equilibrium set to use. exiting")
            raise SystemExit

        # increment density and back through the loop we go
        ρ_init = ρ_init + 1/2000

    if final_only:
        ai_list = ai_list[-1]
        ρ_list = ρ_list[-1]
        mass = 4 / 3 * ρ_list * ai_list[0] * ai_list[1] * ai_list[2]
    else:
        mass = [4 / 3 * ρ * a1 * a2 * a3 for ρ, (a1, a2, a3) in zip(ρ_list, ai_list)]

    return ai_list, mass, [ρ_list, indexs_calculated, no_grav_a1, flag_list]


def index_finder(ρ_list, ρ_wanted):
    """Returns the closest density without going over"""
    for index, ρ in enumerate(ρ_list):
        if ρ < ρ_wanted:
            try:
                if ρ_list[index + 1] > ρ_wanted:
                    return index
            except IndexError:
                print("next rho val is outside of list")
                return -1
