"""setup or run an ngspice simulation """

import subprocess
from pathlib import Path


class Simulate:
    """ngspice simulation"""

    def __init__(self, ngspice_exe: Path, netlist_filename: Path, name: str) -> None:
        self.ngspice_exe: Path = ngspice_exe
        self.netlist_filename: Path = netlist_filename
        self.name: str = name

    @property
    def ngspice_command(self) -> list[str]:
        """define the ngspice command"""
        return [str(self.ngspice_exe), "-b", str(self.netlist_filename)]

    def __str__(self) -> str:
        return " ".join(self.ngspice_command)

    def run(self) -> None:
        """Execute the ngspice simulation."""
        completed_sim = subprocess.run(
            self.ngspice_command, capture_output=True, check=True, text=True
        )

        print(f"return code: {completed_sim.returncode}")

        # NOTE; change this to return the output. Or maybe do something else with it.
        print(completed_sim.stdout)
