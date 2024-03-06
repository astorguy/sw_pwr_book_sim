"""Example from Power Supply book: Section 1.04.04 Linear Regulator"""

# region imports
import tomllib
from pathlib import Path
from typing import Any, Tuple

# endregion

# region global variables
# location of config.toml file and project name table name
TOML_FILENAME: str = "/workspaces/sw_pwr_book_sim/python/config.toml"
PROJ_NAME: str = "sec_1_04_04"


# endregion


# region read toml file
def load_toml(file_to_read: Path) -> dict[str, Any]:
    """read a toml file"""
    with open(file_to_read, "rb") as file:
        toml_data: dict = tomllib.load(file)
    return toml_data


# endregion


# region initialization
def initialize(tom_filename: str, project: str) -> Tuple[Path, Path]:
    config: dict[str, Any] = load_toml(Path(tom_filename))
    ngspice_exe: Path = Path(config["global"]["ngspice_exe_str"])
    proj_path: Path = Path(config["sec_1_04_04"]["proj_path_str"])
    return (ngspice_exe, proj_path)


# endregion


def main() -> None:
    ngspice_exe, proj_path = initialize(TOML_FILENAME, PROJ_NAME)
    print(ngspice_exe)
    print(proj_path)


if __name__ == "__main__":
    main()
