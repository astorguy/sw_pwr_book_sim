"""setup or run an ngspice simulation """

import logging
import subprocess
from pathlib import Path


class Simulate:
    """ngspice simulation"""

    def __init__(self, ngspice_exe: Path, netlist_filename: Path) -> None:
        self.ngspice_exe: Path = ngspice_exe
        self.netlist_filename: Path = netlist_filename

    @property
    def ngspice_command(self) -> list[str]:
        """define the ngspice command"""
        return [str(self.ngspice_exe), "-b", str(self.netlist_filename)]

    def __str__(self) -> str:
        return " ".join(self.ngspice_command)

    def run(self) -> None:
        """Execute the ngspice simulation."""
        try:
            subprocess.run(self.ngspice_command, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running ngspice simulation: {e}")
