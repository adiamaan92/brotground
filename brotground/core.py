"""Brot core module

Iterate Diverge is the core function for all the brot, where the convergence and
divergence of each point on the complex plain is calculated.

This module contains one such implementation of iterate_diverge using numba.
Numba helps us to write the pseudo-code 'as-is' without crazy numpy tricks to achieve peak performance.
This provides core readability and maintainability.

This is just an example of the core implementation. Users can provide their own core as a function while
initializing the brot.
"""
from typing import Callable

import numba as nb


@nb.jit(nopython=True, nogil=True, fastmath=True, parallel=True)
def nb_iterate_diverge(
    x,
    y,
    array,
    threshold: float,
    max_iterations: int,
    brot_equation: Callable,
    divergence_condition: Callable,
    c_initialization: Callable,
    z_initialization: Callable,
):
    """Numba optimized iterate diverge core logic

    Args:
        x ([np.ndarray]): X axis of the brot
        y ([np.ndarray]): Y axis of the brot
        array ([np.ndarray]): Array containing the brot state
        threshold (float): Threshold for divergence
        max_iterations (int): Maximum number of iterations
        brot_equation (Callable): numba optimized brot equation
        divergence_condition (Callable): numba optimized divergence condition
        c_initialization (Callable): numba optimized c initialization
        z_initialization (Callable): numba optimized z initialization

    Returns:
        [type]: [description]
    """
    for i in nb.prange(x.shape[0]):
        for j in range(y.shape[0]):
            z = z_initialization(x[i], y[j])
            c = c_initialization(x[i], y[j])
            n = 0

            while divergence_condition(z) and n <= max_iterations:
                z = brot_equation(z, c)
                n += 1

            array[j, i] = n
    return array
