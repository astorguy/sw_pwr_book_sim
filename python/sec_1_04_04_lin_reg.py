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


# region initialize
def load_config(file_to_read: Path = Path("./config.toml")) -> dict[str, Any]:
    """Read a config file in toml format and return a dictionary with the data.
    If Path to file not given, read ./config.toml.
    """
    with open(file_to_read, "rb") as file:
        toml_data: dict[str, Any] = tomllib.load(file)
    return toml_data


def initialize(config_filename: str, project: str) -> Tuple[Path, Path]:
    """Initialize to get ready for a simulation

    Args:
        config_filename (str): full path with configuration file
        project (str): project name; determines table to read in config file

    Returns:
        Tuple[Path, Path]: returns info needed for subsequent steps
    """

    # Read configuration file and set paths to Ngspice and project
    config: dict[str, Any] = load_config(Path(config_filename))
    ngspice_exe: Path = Path(config["global"]["ngspice_exe_str"])
    proj_path: Path = Path(config[project]["proj_path_str"])

    return (ngspice_exe, proj_path)


# endregion

# region simulate


def simulate(ngspice_exe: Path) -> str:
    print(ngspice_exe)
    return "done"


# endregion


def main() -> None:
    ngspice_exe, proj_path = initialize(TOML_FILENAME, PROJ_NAME)
    print(proj_path)
    finished: str = simulate(ngspice_exe)
    print(finished)


if __name__ == "__main__":
    main()
