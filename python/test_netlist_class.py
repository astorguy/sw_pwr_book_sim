from pathlib import Path
import py4spice as spi

# Path to my project
PROJ_PATH = Path("/workspaces/sw_pwr_book_sim/circuits/simple_rc")
NETLISTS_PATH: Path = PROJ_PATH / "netlists"

fred = spi.Netlist(NETLISTS_PATH / "netlist_file_example.cir")
print(fred)
print("")
# fred.delete_line(2)
# print(fred)
# print("")
# print(f"the index is: {fred.line_starts_with("* a sec")}")
fred.delete_line.
fred.delete_line(fred.line_starts_with("* a sec"))
print(fred)
