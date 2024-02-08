# Create a class called Netlist.
# The data for the class is a list of a list of strings.
# Here is an example of a text file read into the class with __init__:
# * my circuit
# R1 N2 N2 100
# R2 N2 0 200
# VIN N1 0 DC 10V
# Here is an example of the resulting data structure upon reading in the file:
# [["* my circuit"],
# ["R1","N2", "N2", "100"],
# ["R2," "N2", "0", "200"],
# ["VIN", "N1", "0", "DC", "10V"]]
# The first list is a comment and the next three lists are resistors and a voltage source.
# Notice the elements of the internal list normallly do not have white space
# When we initialize the class, we will optionallly pass a filename with will be a text file with each line of the file being a member of the outer list.
# If the line is a comment, denoted by a * in the first column, the line will be a member of the outer list.
# If the line begins with a letter, each word will be a member of the inner list
# We will use type hinting for the class and the methods.
# We will use pathlib for the filename.

import pathlib as Path
from typing import Optional

class Netlist:
    def __init__(self, filename: Optional[Path] = None):
        self.filename = filename
        self.data = [[]]
        if filename:
            self.read_file(filename)



