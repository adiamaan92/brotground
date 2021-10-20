from typing import Callable

import numba as nb
import numpy as np

from brots.BrotBase import BrotBase
from brots.core import nb_iterate_diverge
from brots.project_types import RangeType
from brots.resources import quadratic_julia_set


class UserBrot(BrotBase):
    def __init__(
        self,
        x_range: RangeType = (-2, 2),
        y_range: RangeType = (-2, 2),
        resolution: int = 1000,
        dtype=np.uint16,
        core: Callable = None,
        brot_equation: Callable = None,
        divergence_condition: Callable = None,
        c_initialization: Callable = None,
        z_initialization: Callable = None,
    ):

        if brot_equation is None:

            def multibrot_equation(z: complex, c: complex):
                return z ** 2 + c

            brot_equation = nb.jit(nopython=True, nogil=True, fastmath=True)(
                multibrot_equation
            )

        self._brot_equation = brot_equation

        if divergence_condition is None:

            def default_divergence_condition(z: complex):
                return np.abs(z) < 2

            divergence_condition = nb.jit(nopython=True, nogil=True, fastmath=True)(
                default_divergence_condition
            )

        self._divergence_condition = divergence_condition

        if c_initialization is None:

            def default_initialization(i, j):
                return complex(i, j)

            c_initialization = nb.jit(nopython=True, nogil=True, fastmath=True)(
                default_initialization
            )

        self._c_initialization = c_initialization

        if z_initialization is None:

            def default_initialization(i, j):
                return 0

            z_initialization = nb.jit(nopython=True, nogil=True, fastmath=True)(
                default_initialization
            )

        self._z_initialization = z_initialization

        if core is None:
            core = nb_iterate_diverge

        self._core = core
        super(UserBrot, self).__init__(x_range, y_range, resolution, dtype)

    def iterate_diverge(self, threshold: int = 2, max_iterations: int = 25):
        self._array = self._core(
            self._x,
            self._y,
            self._array,
            threshold,
            max_iterations,
            self._brot_equation,
            self._divergence_condition,
            self._c_initialization,
            self._z_initialization,
        )

    def set_brot_equation(self, equation: Callable):
        self._brot_equation = equation

    def set_c_initialization(self, equation: Callable):
        self._c_initialization = equation

    def set_z_initialization(self, equation: Callable):
        self._z_initialization = equation

    def set_divergence_condition(self, equation: Callable):
        self._divergence_condition = equation


class MultiBrot(UserBrot):
    def __init__(
        self,
        x_range: RangeType = (-2, 2),
        y_range: RangeType = (-2, 2),
        resolution: int = 1000,
        dtype=np.uint16,
        exponent: float = 3,
    ):
        def multibrot_equation(z: complex, c: complex, exponent: float = exponent):
            return z ** exponent + c

        brot_equation = nb.jit(nopython=True, nogil=True, fastmath=True)(
            multibrot_equation
        )
        super(MultiBrot, self).__init__(
            x_range, y_range, resolution, dtype, brot_equation=brot_equation
        )


class MandelBrot(MultiBrot):
    def __init__(
        self,
        x_range: RangeType = (-2, 1),
        y_range: RangeType = (-1.5, 1.5),
        resolution: int = 1000,
        dtype=np.uint16,
    ):
        super(MandelBrot, self).__init__(x_range, y_range, resolution, dtype, 2)


class JuliaBrot(UserBrot):
    def __init__(
        self,
        x_range: RangeType = (-2, 2),
        y_range: RangeType = (-2, 2),
        resolution: int = 1000,
        dtype=np.uint16,
        julia_definition: Callable = None,
        julia_name: str = None,
    ):
        def z_initialization(i, j):
            return complex(i, j)

        custom_z_initialization = nb.jit(nopython=True, nogil=True, fastmath=True)(
            z_initialization
        )

        if julia_definition is None:

            if julia_name is None:
                default_julia = quadratic_julia_set["frost_fractal"]

                def c_initialization(i, j):
                    return default_julia

                julia_definition = nb.jit(nopython=True, nogil=True, fastmath=True)(
                    c_initialization
                )
            else:
                default_julia = quadratic_julia_set[julia_name]

                def c_initialization(i, j):
                    return default_julia

                julia_definition = nb.jit(nopython=True, nogil=True, fastmath=True)(
                    c_initialization
                )

        super(JuliaBrot, self).__init__(
            x_range,
            y_range,
            resolution,
            dtype,
            c_initialization=julia_definition,
            z_initialization=custom_z_initialization,
        )
