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

    def vec_subset(self, vecs: list[str]) -> None:
        """create a smaller subset of the header vectors

        Args:
            vecs (list[str]): vector subset
        """
        if set(vecs).issubset(self.header):
            indices_for_deletion = [
                index for index, item in enumerate(self.header) if item not in vecs
            ]
            indices_for_deletion.sort(reverse=True)
            del indices_for_deletion[-1]  # remove index 0 (x-axis) from list

            # Delete header names & data columns, starting from end, working backwards
            for i in indices_for_deletion:
                del self.header[i]
                self.data = np.delete(self.data, i, axis=1)
        else:
            print("Error: vecs is not a subset of the header list")

    def x_range(self, x_begin: float, x_end: float, npts: int = 1000) -> None:
        """Limit range of data and create linear-spaced points

        Args:
            x_begin (float): new x start
            x_end (float): new x end
            npts (int): number of linear points in new array
        """
        x_orig = self.data[:, 0]
        y_origs = self.data[:, 1:]
        x_new = np.linspace(x_begin, x_end, npts)
        new_array = np.zeros((npts, y_origs.shape[1] + 1))
        new_array[:, 0] = x_new

        # Interpolate y columns using interp1d
        for i in range(y_origs.shape[1]):
            funct = interp1d(x_orig, y_origs[:, i])
            new_array[:, i + 1] = funct(x_new)

        self.data = new_array
