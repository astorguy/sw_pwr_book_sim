"""initialize and run Kicad cmd"""
import subprocess
from subprocess import CompletedProcess
from pathlib import Path


class Kicad:
    """KiCad netlist export command"""

    def __init__(
        self, kicad_cmd: Path, sch_filename: Path, netlist_filename: Path
    ) -> None:
        self.kicad_cmd: Path = kicad_cmd  # Path to the KiCad executable
        self.sch_filename: Path = sch_filename
        self.netlist_filename: Path = netlist_filename

        # construct the command
        self.cmd_args: list[str] = [f"{self.kicad_cmd}"]
        self.cmd_args.append("sch")
        self.cmd_args.append("export")
        self.cmd_args.append("netlist")
        self.cmd_args.append("--output")
        self.cmd_args.append(f"{self.netlist_filename}")
        self.cmd_args.append("--format")
        self.cmd_args.append("spice")
        self.cmd_args.append(f"{self.sch_filename}")
        self.cmd: str = " ".join(str(item) for item in self.cmd_args)

    def __str__(self) -> str:
        """print out the constructed KiCad cmd

        Returns:
            str: the cmd that has been contructed
        """
        return self.cmd

    def run(self) -> CompletedProcess[bytes]:
        """execute the kicad cmd"""
        return subprocess.run(self.cmd_args, check=False)

    def delete_forward_slashes(self) -> None:
        """Delete forward slashes from all node names in the netlist file."""

        # Open the file for reading and writing
        with open(self.netlist_filename, "r+") as file:
            lines: list[str] = file.readlines()  # Read the lines
            file.seek(0)  # Move the file pointer back to the beginning

            # Iterate through each line
            for line in lines:
                # Check if the line starts with a letter
                if line[0].isalpha():
                    # Split the line into words
                    words: list[str] = line.split()
                    # Remove the forward slash from each word that starts with it
                    words = [
                        word[1:] if word.startswith("/") else word for word in words
                    ]
                    # Join the words back together into a line
                    line: str = " ".join(words) + "\n"
                # Write the modified line back to the file
                file.write(line)

            # Truncate the file to the current position to remove any leftover content
            file.truncate()
