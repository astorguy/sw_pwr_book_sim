"""Multiple y signals vs an x-axis"""

from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d
from .globals_types import numpy_flt


class Signals:
    """Object hold multiple y signals vs an x-axis. This data can be plotted y's vs x.
    It can also hold table data when X-Axis set = NO_X_AXIS
    """

    def __init__(
        self,
        x_data: list[float | int],
        y_data_list: list[list[float | int]],
        x_label: str,
        y_labels: list[str],
    ):
        self.x_data = np.array(x_data, dtype=float)
        self.y_data_list = [np.array(y_data, dtype=float) for y_data in y_data_list]
        self.x_label = str(x_label)
        self.y_labels = y_labels

    def __repr__(self) -> str:
        return_string = f"Signals(x_data={self.x_data.tolist()}, "
        return_string += f"y_data_list={self.y_data_list}, "
        return_string += f"x_label='{self.x_label}', "
        return_string += f"y_labels={self.y_labels}"
        return return_string

    @staticmethod
    def _delete_columns(
        col_name: str, y_labels_in: list[str], y_data_in: list[list[float]]
    ) -> tuple[list[str], list[list[float]]]:
        # if no dup columns, just return the input values
        if col_name not in y_labels_in:
            return y_labels_in, y_data_in

        # identify columns to delete
        col_indices = [i for i, label in enumerate(y_labels_in) if label == col_name]
        col_indices.reverse()  # Reverse the list to delete columns from right to left

        # initialize to return all columns
        y_labels_return = y_labels_in.copy()
        y_data_return = y_data_in.copy()

        for col_index in col_indices:
            del y_labels_return[col_index]  # Remove the column(s) from y_labels
            del y_data_return[col_index]  # Remove the column(s) from y_data_return

        return y_labels_return, y_data_return

    @classmethod
    def from_spice_plot(cls, filename: Path) -> "Signals":
        """something"""

        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Extract the first line and split it by whitespace into a list of strings
        first_line = lines[0].split()
        x_label = first_line[0]
        y_labels = first_line[1:]

        # Convert rest of the data to numpy float
        data = [line.split() for line in lines[1:]]
        float_array = np.array(data, dtype=float)
        x_data = float_array[:, 0]
        y_data_list = float_array[:, 1:].T.tolist()

        # Ngspice puts in these extra x-axes columns for no good reason
        # delete additional x-axes columns in data
        y_labels, y_data_list = Signals._delete_columns(x_label, y_labels, y_data_list)

        return cls(x_data, y_data_list, x_label, y_labels)

    @classmethod
    def from_spice_table(cls, filename: Path) -> "Signals":
        """something"""

        # read in the file contents
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        y_labels = [line.split()[0] for line in lines]
        y_numbers = [float(line.split()[-1]) for line in lines]
        y_data_list = [np.array(y_number, dtype=float) for y_number in y_numbers]

        return cls([0.0], y_data_list, "", y_labels)

    def signal_value(self, sig_name: str, x_value: float = 0.0) -> float:
        """Print out the signal at x_value

        Returns:
            float: the value of the signal at that X value
        """
        index = self.y_labels.index(sig_name)

        # if only 1 x-axis value
        if len(self.x_data) == 1:
            y_value = self.y_data_list[index]
            return y_value

        # otherwise, there are multiple x values
        x_values = self.x_data
        y_values = self.y_data_list[index]
        funct = interp1d(x_values, y_values)
        y_value = funct(x_value)
        return y_value

    def signals_table(self, sig_names: list[str], x_value: float = 0.0) -> str:
        """Create a table of values for all the sig_names at a point along x-axis.

        Args:
            sig_names (list[str]): signals to include in table
            x_value (float, optional): X-axis value. Defaults to 0.0.

        Returns:
            str: A table listing the values.
        """
        y_value_column_start = len(max(sig_names, key=len))

        lines = [f"Signal values for x = {x_value:.6g}"]
        for sig_name in sig_names:
            y_value = self.signal_value(sig_name, x_value)
            if y_value < 0:
                line = f"{sig_name.rjust(y_value_column_start)}: {y_value:.6g}"
            else:
                line = f"{sig_name.rjust(y_value_column_start)}:  {y_value:.6g}"
            lines.append(line)
        return "\n".join(lines)

    def x_axis_and_sigs(
        self, signal_names: list[str]
    ) -> list[numpy_flt, list[numpy_flt]]:
        """Returns X-Axis numpy and numpys for all the signals

        Args: signal names of numpy's to return with X-axis

        Returns:
            _type_: list of the X-axis numpy and list of signals numpy's
        """
        y_signals = []
        for signal_name in signal_names:
            index = self.y_labels.index(signal_name)
            signal_data = self.y_data_list[index]
            y_signals.append(signal_data)
        return [self.x_data, y_signals]
