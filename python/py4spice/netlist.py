# Python 3.12
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

from pathlib import Path
from typing import Optional

class Netlist:
    def __init__(self, filename_or_string: Optional[Path | str] = None) -> None:
        self.data: list[str] = []
        if isinstance(filename_or_string, Path):
            with open(filename_or_string, "r") as file:
                self.data = file.readlines()
        if isinstance(filename_or_string, str):
            self.data = filename_or_string.split("\n")

    def write_to_file(self, filename: Path) -> None:
        with open(filename, "w") as file:
            file.writelines(self.data)

    def __add__(self, other: Netlist) -> Netlist:
        return Netlist(self.data + other.data)

    def __str__(self) -> str:
        return "\n".join(self.data)
    
    def insert(self, index: int, value: str) -> None:
        self.data.insert(index, value)

    def append(self, value: str) -> None:
        self.data.append(value)

    def delete_line(self, index: int) -> None:
        del self.data[index]

    def line_begins_with(self, string: str) -> int:
        for index, line in enumerate(self.data):
            if line.startswith(string):
                return index
        return -1
    