"""Convert text file simulation results to objects"""

from pathlib import Path

import numpy as np
from scipy.interpolate import interp1d

from .globals_types import TABLE_DATA, AnaType, numpy_flt


class SimResults:
    """Create objects for results extracted from simulation text files.

    Note: All data has an x-axis as first column in array even if it is table
    data such as "op", "tf", etc. This is done for data consistency
    """

    def __init__(self, analysis_type: AnaType, header: list[str], data: numpy_flt):
        self.analysis_type = analysis_type
        self.header = header
        self.data = data

    def __str__(self) -> str:
        string1 = f"analysis_type: {self.analysis_type}\n\n"
        string2 = f"header:\n{self.header}\n\n"
        string3 = f"data:\n{self.data}"
        return string1 + string2 + string3

    def __repr__(self) -> str:
        package_name = __package__
        class_name = type(self).__name__
        string = f"{package_name}.{class_name}("
        string += f"analysis_type = {self.analysis_type!r}, "
        string += f"header = {self.header!r}, "
        string += f"data = numpy.{self.data!r})"
        return string

    @staticmethod
    def _table_processing(filename: Path) -> tuple[list[str], numpy_flt]:
        """Convert simulation text data that is in the form of a table.

        Args:
            filename (Path): text file results from a simulation

        Returns:
            tuple[list[str], numpy_flt]: header and footer data
        """
        # Read in each line putting first word into header, last word float
        first_words = ["x-axis"]  # Initialize with x-axis
        last_words = np.array([0.0], dtype=np.float64)  # Initialize with x = 0.0
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                words = line.split()
                if len(words) > 0:
                    first_word = words[0]
                    last_word = float(words[-1])
                    first_words.append(first_word)
                    last_words = np.append(last_words, (last_word))

        header = first_words

        # turn last words to 2d numpy for data consistancy
        data = np.column_stack((last_words,))

        return header, data

    @staticmethod
    def _plot_processing(filename: Path) -> tuple[list[str], numpy_flt]:
        """Convert simulation text data that is in the form of a plot.

        Args:
            filename (Path): text file results from a simulation

        Returns:
            tuple[list[str], numpy_flt]: header and footer data
        """
        # turn first row into list of words for header
        with open(filename, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            header = first_line.split()

        # skip the header and put data to 2d numpy
        data = np.genfromtxt(filename, dtype=float, skip_header=1)

        return header, data

    @staticmethod
    def _find_duplicate_indexes(strings: list[str]) -> list[int]:
        """determine which indices are duplicates

        Args:
            strings (list[str]): simulation text data in

        Returns:
            list[int]: simulation text data in
        """
        duplicate_indexes = []
        seen = set()

        for i, string in enumerate(strings):
            if string in seen:
                duplicate_indexes.append(i)
            else:
                seen.add(string)

        return duplicate_indexes

    @staticmethod
    def _remove_dups(
        header_in: list[str], data_in: numpy_flt
    ) -> tuple[list[str], numpy_flt]:
        """remove duplicate columns before creating an object

        Args:
            header_in (list[str]): header info in text form
            data_in (numpy_flt): 2d numpy of data

        Returns:
            tuple[list[str], numpy_flt]: data ready to make object
        """
        dup_indexes = SimResults._find_duplicate_indexes(header_in)

        # delete dups in data numpy array
        data_without_dups = np.delete(data_in, dup_indexes, axis=1)

        # delete dups from header
        for index in sorted(dup_indexes, reverse=True):
            del header_in[index]
        header_without_dups = header_in

        return header_without_dups, data_without_dups

    @classmethod
    def from_file(cls, analysis_type: AnaType, filename: Path) -> "SimResults":
        """read data from a ngspice simulation file

        Args:
            analysis_type (AnaType): the analysis type of the text sim data
            filename (Path): where is the sim results located

        Returns:
            SimResults: object created
        """
        if analysis_type in TABLE_DATA:
            header, data = cls._table_processing(filename)
            return cls(analysis_type, header, data)

        # otherwise it is plot data
        (header1, data1) = cls._plot_processing(filename)
        (header, data) = cls._remove_dups(header1, data1)
        return cls(analysis_type, header, data)

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

    def x_range(self, x_begin: float, x_end: float, npts: int) -> None:
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

    def print_table(self) -> str:
        """Print out the data for types in table form

        Returns:
            str: output that can be printed
        """
        padding = 3
        second_col_start = len(max(self.header, key=len)) + padding

        lines = []
        lines.extend(
            [
                (
                    f"{h:<{second_col_start - 1}}{d[0]}"
                    if d[0] < 0
                    else f"{h:<{second_col_start}}{d[0]}"
                )
                for h, d in zip(self.header, self.data)
            ]
        )
        lines.pop(0)  # delete the x-axis item
        return "\n".join(lines)

    def single_column(self, signal_name: str) -> numpy_flt:
        """Returns a single Numpy Array for the signal

        Returns:
            _type_: 1D numpy array
        """
        index = self.header.index(signal_name)
        the_column: numpy_flt = self.data[:, index]
        return the_column

    def x_axis_and_sigs(self, signal_names: list[str]) -> list[numpy_flt]:
        """Returns X-Axis numpy and all the signals

        Args: signal names of numpy's to return with X-axis

        Returns:
            _type_: list of the X-axis and signals numpy's
        """

        list_of_numpys = [self.data[:, 0]]  # First, the x-axis (always 1st col.)
        for signal_name in signal_names:
            list_of_numpys.append(self.single_column(signal_name))

        return list_of_numpys

    def table_value(self, signal_name: str) -> float:
        """return the value of the signal. Must be table data.

        Args:
            signal_name (str): what signal to see

        Returns:
            str: value of the table data
        """
        index = self.header.index(signal_name)
        return float(self.data[index][0])

    def add_signal(self, sig_name: str, column_array: numpy_flt) -> None:
        """Adds a another signal to the object

        Args:
            sig_name (str): name of the new sign
            column_array (numpy_flt): numpy 1D column; num of pts must match other sigs
        """
        self.header.append(sig_name)  # add in the name to the header
        self.data = np.column_stack((self.data, column_array))  # add in numpy column

    def rename_signals(self, old_sigs: list[str], new_sigs: list[str]) -> None:
        """rename list of existing signals with the list of new signals

        Args:
            old_sigs (list[str]): existing (old) signals
            new_sigs (list[str]): signals (new) to replace old signals
        """
        for i, sig in enumerate(old_sigs):
            if sig in self.header:
                index = self.header.index(sig)
                self.header[index] = new_sigs[i]

    def multiply(self, factor1_name: str, factor2_name: str, result_name: str) -> None:
        """multiplies the two signals and adds the result to the object

        Args:
            factor1_name (str): signal name of factor1
            factor2_name (str): signal name of factor2
            result_name (str): signal name of the result (added to the object)
        """
        fac1: numpy_flt = self.single_column(factor1_name)
        fac2: numpy_flt = self.single_column(factor2_name)
        result: numpy_flt = fac1 * fac2
        self.add_signal(result_name, result)

    def scaler(self, scalar: float, signal_name: str, result_name: str) -> None:
        """Scalar multiple and adds the result to the object

        Args:
            scalar (float): the scalar
            signal_name (str): sig name to be multiplied
            result_name (str): signal name of the result (added to the object)
        """
        sig = self.single_column(signal_name)
        result = scalar * sig
        self.add_signal(result_name, result)

    def divide(self, dividend_name: str, divisor_name: str, result_name: str) -> None:
        """Divides the dividend by the divisor and adds the result to the object

        Args:
            dividend_name (str): signal name of dividend
            divisor_name (str): signal name of divisor
            result_name (str): signal name of the result (added to the object)
        """
        dividend = self.single_column(dividend_name)
        divisor = self.single_column(divisor_name)
        result = dividend / divisor
        self.add_signal(result_name, result)
