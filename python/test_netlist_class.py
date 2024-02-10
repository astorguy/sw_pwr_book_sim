from pathlib import Path
import py4spice as spi

# Path to my project
PROJ_PATH = Path("/workspaces/sw_pwr_book_sim/circuits/simple_rc")
NETLISTS_PATH: Path = PROJ_PATH / "netlists"

fred = spi.Netlist(NETLISTS_PATH / "netlist_file_example.cir")
print(fred)

fred.write_to_file(NETLISTS_PATH / "zz.cir")

henry = fred + spi.Netlist("the middle") + fred + spi.Netlist("the end")
henry.write_to_file(NETLISTS_PATH / "zzz.cir")
print(henry)
