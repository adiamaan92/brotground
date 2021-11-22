"""List of resources for brot generation

This provides additional brots and julia sets for the project.
This is in no means exhaustive, but it is a good start.
"""
import numba as nb
import numpy as np


@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def tricorn_brot_equation(z: complex, c: complex):
    return np.conjugate(z ** 2) + c


@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def burning_ship_brot_equation(z: complex, c: complex):
    return np.square(np.abs(np.real(z)) + 1j * np.abs(np.imag(z))) + c


@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def sin_brot_equation(z: complex, c: complex):
    return np.sin(z) * c


@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def cos_brot_equation(z: complex, c: complex):
    return np.cos(z) * c


quadratic_julia_set = dict(
    dentrite_fractal=complex(0, 1),
    douadys_rabbit_fractal=complex(-0.123, 0.745),
    san_marco_fractal=complex(-0.750, 0),
    siegel_disk_fractal=complex(-0.391, -0.587),
    cauliflower_fractal=complex(-0.7, 0.3),
    galaxiex_fractal=complex(-0.75, -0.2),
    groovy_fractal=complex(-0.75, 0.15),
    frost_fractal=complex(-0.7, 0.35),
)
