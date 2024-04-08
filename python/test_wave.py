"""test for Waveforms class"""

import numpy as np
import py4spice as spi
import matplotlib.pyplot as plt


# from py4spice.globals_types import numpy_flt


def main() -> None:
    # a1 = spi.Waveforms(
    #     ["x", "y1", "y2"],
    #     np.array(
    #         [[1.0, 2.0, 3.0, 3.5], [30.0, 31.4, 33.8, 29.9], [41.8, 50.2, 39.2, 30.6]], dtype=float
    #     ),
    #     2,
    # )
    # print(a1.header)
    # print(a1.data)

    header = ["x", "y1", "y2", "y3", "y4"]
    x_vals = [1.1, 1.3, 1.5, 1.8, 2.0]
    y1_vals = [3.4, 3.2, 3.11, 3.4, 3.6]
    y2_vals = [2.4, 4.2, 4.11, 4.4, 4.6]
    y3_vals = [8.4, 5.2, 5.11, 5.4, 5.6]
    y4_vals = [66.4, 6.2, 6.11, 6.4, 6.6]

    data_non_linear_spacing = np.vstack([x_vals, y1_vals, y2_vals, y3_vals, y4_vals]).T

    # print(header)
    # print(data_non_linear_spacing)

    a1 = spi.Waveforms(header, data_non_linear_spacing)

    # Create a new figure
    plt.figure()

    # Get the x-values (first column of data)
    my_x = a1.data[:, 0]

    # Plot each y-values array against x-values
    for i in range(1, a1.data.shape[1]):
        plt.plot(my_x, a1.data[:, i], label=f"y{i}")

    # Add a legend
    plt.legend()

    # Save the figure as a PNG file
    plt.savefig("plot.png")


if __name__ == "__main__":
    main()
