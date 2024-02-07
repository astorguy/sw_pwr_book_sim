# Create a class called Netlist.
# The data for the class is a list of a list of strings.

import pathlib as Path
from typing import Optional


class Netlist:
    def __init__(self):
        self.netlist_data: list[list[str]] = [[""]]
