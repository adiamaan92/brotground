"""Brots module that contains the UserBrot, MultiBrot, MandelBrot
and JuliaBrot definitions

UserBrot: This is the base brot that is used to create all other brots.
This will default to a mandelbrot.

MultiBrot: This is similar to UserBrot, but instead of Z^2 + C,
it will use a parameter as the exponent, making it Z^k + C.
Everything else remains the same.

ManderlBrot: This is the same as UserBrot and inherits from Multibrot.
Added as a class separately so that it is evident for API usage.

JuliaBrot: This uses the mandelbrot equation but changes the Z and C
initialization. Usually Z is initialized as 0, but in JuliaSet, it is 
initialized as complex number of (i, j). Similarly, C is initialized as
a complex number of (i, j), whereas in Julia set it is set constant based on
the type of JuliaSet you are trying to generate.

"""
from typing import Callable

import numba as nb
import numpy as np

from brotground.BrotBase import BrotBase
from brotground.core import nb_iterate_diverge
from brotground.project_types import RangeType
from brotground.resources import quadratic_julia_set


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
        """UserBrot constructor

        Args:
            x_range (RangeType, optional): [description]. Defaults to (-2, 2).

            y_range (RangeType, optional): [description]. Defaults to (-2, 2).

            resolution (int, optional): [description]. Defaults to 1000.

            dtype ([type], optional): [description]. Defaults to np.uint16. Directly proportional
                to the run time of convergence.

            All the equations default to  is done this way instead of passing the function as default argument to
            get around the shortcoming of passing numba compiled function as argument.

            core (Callable, optional): [description]. The iterate_diverge logic.
                If not given the numba compiled logic will be taken as default.

            brot_equation (Callable, optional): Equation that governs the brot generation. Defaults to
                Mandelbrot equation, which is Z^2 + C.

            divergence_condition (Callable, optional): Divergence condition that marks which points
                have diverged. Defaults to abs(z) < 2.

            c_initialization (Callable, optional): C Initializaiton, defaulting to complex(i, j)

            z_initialization (Callable, optional): Z Initialization, defaulting to 0.

        Returns:
            [type]: [description]
        """

        if brot_equation is None:

            def mandelbrot_equation(z: complex, c: complex):
                return z ** 2 + c

            brot_equation = nb.jit(nopython=True, nogil=True, fastmath=True)(
                mandelbrot_equation
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
        """Iterate and diverge function that calls the core function.

        Args:
            threshold (int, optional): Defaults to 2. That controls the divergence condition.
            max_iterations (int, optional): Defaults to 25. That controls the max iteration.

            Both threshold and max_iteration are used to control the convergence.
        """
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
        """
            This is similar to UserBrot, but instead of Z^2 + C,
            it will use a parameter as the exponent, making it Z^k + C.
            Everything else remains the same.

        Args:
            x_range (RangeType, optional): [description]. Defaults to (-2, 2).
            y_range (RangeType, optional): [description]. Defaults to (-2, 2).
            resolution (int, optional): [description]. Defaults to 1000.
            dtype ([type], optional): [description]. Defaults to np.uint16.
            exponent (float, optional): [description]. Defaults to 3.
        """

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
        """This is the same as UserBrot and inherits from Multibrot.
        Added as a class separately so that it is evident for API usage.

        Args:
            x_range (RangeType, optional): [description]. Defaults to (-2, 1).
            y_range (RangeType, optional): [description]. Defaults to (-1.5, 1.5).
            resolution (int, optional): [description]. Defaults to 1000.
            dtype ([type], optional): [description]. Defaults to np.uint16.
        """
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
        """
        This uses the mandelbrot equation but changes the Z and C
        initialization. Usually Z is initialized as 0, but in JuliaSet, it is
        initialized as complex number of (i, j). Similarly, C is initialized as
        a complex number of (i, j), whereas in Julia set it is set constant based on
        the type of JuliaSet you are trying to generate.

        Args:
            x_range (RangeType, optional): [description]. Defaults to (-2, 2).
            y_range (RangeType, optional): [description]. Defaults to (-2, 2).
            resolution (int, optional): [description]. Defaults to 1000.
            dtype ([type], optional): [description]. Defaults to np.uint16.
            julia_definition (Callable, optional): [description]. Defaults to None.
            julia_name (str, optional): [description]. Defaults to None.
        """

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
