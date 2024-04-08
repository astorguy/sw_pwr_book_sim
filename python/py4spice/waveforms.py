""" Waveforms with a single x value and one or more y values in a 2D numpy array.
    header defines the column names."""

import numpy as np
from scipy.interpolate import interp1d  # type: ignore

from .globals_types import numpy_flt


class Waveforms:
    def __init__(self, header: list[str], data: numpy_flt, npts: int = 1000):
        self.header: list[str] = header

        column_count: int = data.shape[1]  # number of columns
        x: numpy_flt = data[:, 0]  # first column array
        self.data: numpy_flt = np.zeros((npts, column_count))  # initialize data array
        self.data[:, 0] = np.linspace(x[0], x[-1], npts)  # generate x-values

        # interpolate y-values for each column
        for i in range(1, column_count):
            y: numpy_flt = data[:, i]
            f = interp1d(x, y)
            self.data[:, i] = f(self.data[:, 0])

    @property
    def npts(self) -> int:
        return self.data.shape[0]
