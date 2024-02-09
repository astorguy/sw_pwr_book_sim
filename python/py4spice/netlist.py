# Create a class called Netlist.
# Use type hinting for the class and the methods.
# Use pathlib for the filename.
# The data for the class is a list of strings.
# The class should have an __init__ method that takes a filename as an argument, or a string, or nothing.
# Here is an example of a text file read into the class with __init__:
# * my circuit
# R1 N2 N2 100
# R2 N2 0 200
# VIN N1 0 DC 10
# Here is an example of the resulting data structure upon reading in the file:
# ["* my circuit","R1 N2 N2 100","R2 N2 0 200","VIN N1 0 DC 10"]
# Add a method to the class that will write the data to a file.
# netlist objects can be added with the + operator.

from typing import List, Optional
from pathlib import Path

class Netlist:
    