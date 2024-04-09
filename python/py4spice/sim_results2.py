"""Convert text file simulation results to objects"""

from pathlib import Path

import numpy as np

from .globals_types import TABLE_DATA, AnaType, numpy_flt


class SimResults2:
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
        duplicate_indexes: list[int] = []
        seen: set[str] = set()

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
        dup_indexes: list[int] = SimResults2._find_duplicate_indexes(header_in)

        # delete dups in data numpy array
        data_without_dups = np.delete(data_in, dup_indexes, axis=1)

        # delete dups from header
        for index in sorted(dup_indexes, reverse=True):
            del header_in[index]
        header_without_dups = header_in

        return header_without_dups, data_without_dups

    @classmethod
    def from_file(cls, analysis_type: AnaType, filename: Path) -> "SimResults2":
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
