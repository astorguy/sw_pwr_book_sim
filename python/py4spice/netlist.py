from pathlib import Path
from typing import Optional


class Netlist:
    def __init__(self, filename_or_string: Optional[Path | str] = None) -> None:
        self.data: list[str] = []
        if isinstance(filename_or_string, Path):
            with open(filename_or_string, "r") as file:
                self.data = [line.rstrip("\n") for line in file.readlines()]
        if isinstance(filename_or_string, str):
            self.data = filename_or_string.split("\n")

    def __str__(self) -> str:
        return "\n".join(self.data)

    def write_to_file(self, filename: Path) -> None:
        with open(filename, "w") as file:
            file.write("\n".join(self.data))

    def __add__(self, other: "Netlist") -> "Netlist":
        combined_data = self.data + other.data
        return Netlist("\n".join(combined_data))

