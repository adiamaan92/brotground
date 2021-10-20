"""Brot superclass for all brots

This class contains functions and utilities that all the brots need. Classes
inherited from this superclass are:

Constructor:
    - init - initializes the brot with x and yrange, resolution, dtype

Utilities:
    - get_shape - gets the shape of the brot
    - fetch_array - fetches the 2D array that is used to store the brot state
    - reset - resets the brot to its initial state

Setters:
    - set_range - sets the x and y range of the brot
    - set_axes - sets the x and y axes of the brot based on the resolution
    - set_boundaries - sets the boundaries of the brot based on the x and y range given
    - set_array - zero initialize the brot state
    - set_resolution - sets the resolution of the brot

Abstract methods:
    - iterate_diverage - the core logic of generating the brot. Any brot inheriting from BrotBase
    must implement this method.
"""

from abc import abstractmethod

import numpy as np

from brots.project_types import RangeType


class BrotBase:
    def __init__(self, x_range: RangeType, y_range: RangeType, resolution: int, dtype):
        self._x_range = x_range
        self._y_range = y_range
        self._resolution = resolution
        self._dtype = dtype

        self._x: np.ndarray
        self._y: np.ndarray
        self._array: np.ndarray

        self.reset(dtype=self._dtype)

    def get_shape(self):
        """Returns the shape of the brot array state

        Returns:
            [Tuple[int, int]]: The shape of the brot array state
        """
        return self._array.shape

    def fetch_array(self):
        """Copies the array state and returns it so that it can be overwritten
        without affecting the orignal state

        Returns:
            [np.ndarray]: copy of the brot array state
        """
        return self._array.copy()

    def reset(self, dtype=np.uint16):
        """Resets the brot

        Args:
            dtype ([type], optional): [description]. Defaults to np.uint16.
        """
        self.set_axes()

    def set_range(self, x_range: RangeType, y_range: RangeType):
        """Sets the x and y range of the brot

        Args:
            x_range (RangeType): X range of the brot
            y_range (RangeType): Y range of the brot
        """
        self._x_range = x_range
        self._y_range = y_range
        self.reset()

    # Setter functions
    def set_axes(self):
        """Sets the x and y axes of the brot based on the resolution
        A evenly spaced array is created between x and y range based on
        the resolution of the brot
        """
        self._x = np.linspace(self._x_range[0], self._x_range[1], self._resolution)
        self._y = np.linspace(self._y_range[0], self._y_range[1], self._resolution)
        self.set_array(dtype=self._dtype)

    def set_boundaries(self, x_range: RangeType, y_range: RangeType):
        """Set boundaries for the brot

        Args:
            x_range (RangeType): X boundary
            y_range (RangeType): Y boundary
        """
        self._x_range = x_range
        self._y_range = y_range
        self.reset(dtype=self._dtype)

    def set_array(self, dtype=np.uint16):
        """Sets the brot array state to zero

        Args:
            dtype ([type], optional): [description]. Defaults to np.uint16.
        """
        self._array = np.zeros(shape=(self._resolution, self._resolution), dtype=dtype)

    def set_resolution(self, resolution: int):
        """Set the resolution of the brot.
        This action resets the brot state.

        Args:
            resolution (int): resolution of the brot
        """
        self._resolution = resolution
        self.reset(dtype=self._dtype)

    @abstractmethod
    def iterate_diverge(self):
        """Abstract method that any brot inheriting from BrotBase must implement."""
        pass
