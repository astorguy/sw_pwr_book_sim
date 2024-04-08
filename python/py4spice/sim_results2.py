"""Convert text file simulation results to objects"""

from pathlib import Path

import numpy as np
from scipy.interpolate import interp1d

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
