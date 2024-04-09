from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from scipy.interpolate import interp1d  # type: ignore

numpy_flt: TypeAlias = npt.NDArray[np.float64]


class Waveforms:
    """Waveforms with a single x value and one or more y values in a 2D numpy array.
    header defines the column names."""

    def __init__(self, header: list[str], data: numpy_flt, npts: int = 1000):
        self.header: list[str] = header

        column_count: int = data.shape[1]  # number of columns
        self.data: numpy_flt = np.zeros((npts, column_count))
        self.data[:, 0] = np.linspace(data[0, 0], data[-1, 0], npts)

        # interpolate y-values for each column
        x: numpy_flt = data[:, 0]
        for i in range(1, column_count):
            y: numpy_flt = data[:, i]
            f = interp1d(x, y)
            self.data[:, i] = f(self.data[:, 0])

    @property
    def npts(self) -> int:
        """number of data points (rows) in the waveform"""
        return self.data.shape[0]
