""" Initialize and run Kicad-cli command to generate SPICE netlist
    This program works best if it is placed in the same directory as the schematic file.
    The resulting netlist will be placed in the same directory as the schematic file.
    IMPORTANT: set the name of the schematic to read (the SCH_NAME variable)
"""

import subprocess
from pathlib import Path
from subprocess import CompletedProcess

# IMPORTANT: set the name of the schematic to read
SCH_NAME = "sec_1_04_04_lin_reg"

# Kicad cammand line executable
KICAD_CMD = Path("C:/Program Files/KiCad/7.0/bin/kicad-cli.exe")

SCH_FILENAME = Path(".") / f"{SCH_NAME}.kicad_sch"
NETLIST_FILENAME = Path(".") / "raw_kicad.cir"


class Kicad:
    """KiCad netlist export command"""

    def __init__(
        self, kicad_cmd: Path, sch_filename: Path, netlist_filename: Path
    ) -> None:
        self.kicad_cmd: Path = kicad_cmd
        self.sch_filename: Path = sch_filename
        self.netlist_filename: Path = netlist_filename

        # construct the command
        self.cmd_args = [f"{self.kicad_cmd}"]
        self.cmd_args.append("sch")
        self.cmd_args.append("export")
        self.cmd_args.append("netlist")
        self.cmd_args.append(f"--output")
        self.cmd_args.append(f"{self.netlist_filename}")
        self.cmd_args.append("--format")
        self.cmd_args.append("spice")
        self.cmd_args.append(f"{self.sch_filename}")
        self.cmd: str = " ".join(str(item) for item in self.cmd_args)

    def __str__(self) -> str:
        """print out the constructed KiCad cmd"""
        return self.cmd

    def run(self) -> CompletedProcess[bytes]:
        """execute the kicad cmd"""
        return subprocess.run(self.cmd_args, check=False)


def main() -> None:
    """main"""

    # construct the kicad cmd
    my_kicadcmd = Kicad(KICAD_CMD, SCH_FILENAME, NETLIST_FILENAME)
    print(my_kicadcmd)  # print out the kicad cmd, though not necessary
    my_kicadcmd.run()  # run the kicad cmd


if __name__ == "__main__":
    main()
