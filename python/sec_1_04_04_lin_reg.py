"""Example from Power Supply book: Section 1.04.04 Linear Regulator"""

# region imports
import tomllib
from pathlib import Path
from typing import Any

import py4spice as spi

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


def define_paths(ngspice_exe: Path, proj_path: Path) -> dict[str, Path]:
    """Define all the paths needed for the project
    based on the project path"""

    # Create dictionary of paths, starting with ngspice_exe and proj_path
    paths: dict[str, Path] = {"ngspice_exe": ngspice_exe, "proj_path": proj_path}

    # Create sim_results directory if doesn't exist
    results_path: Path = proj_path / "sim_results"
    results_path.mkdir(parents=True, exist_ok=True)
    paths["results_path"] = results_path  # Add to dictionary

    # Create netlists directory and files if they don't exist
    netlists_path: Path = proj_path / "netlists"
    netlists_path.mkdir(parents=True, exist_ok=True)  # Create the directory
    paths["netlists_path"] = netlists_path  # Add to dictionary

    return paths


def define_vector_sets() -> list[spi.Vectors]:
    """Define all the vector sets for simulation and post-simulation analysis

    Returns:
        list[spi.Vectors]: list of all the vector sets defined here
    """
    vec_all = spi.Vectors("all")
    vec_in_out = spi.Vectors("in out")
    return [vec_all, vec_in_out]


def initialize(config_filename: str, project: str) -> None:
    """Initialize items that won't change during simulation and post-simulation
    analysis

    Args:
        config_filename (str): full path to configuration file
        project (str): project name; determines table to read in config file

    Returns:
        write something here
    """

    # Read configuration file and set paths to Ngspice and project
    config: dict[str, Any] = load_config(Path(config_filename))
    ngspice_exe: Path = Path(config["global"]["ngspice_exe_str"])
    proj_path: Path = Path(config[project]["proj_path_str"])

    # create dictionary of paths including ngspice_exe and proj_path
    my_paths: dict[str, Path] = define_paths(ngspice_exe, proj_path)

    # list_of_vectors: list[spi.Vectors] = define_vector_sets()


# endregion

# region simulate


def simulate(ngspice_exe: Path, netlist: Path) -> str:

    # prepare simulate object, print out command, and simulate
    sim1: spi.Simulate = spi.Simulate(ngspice_exe, netlist)
    # spi.print_section("Ngspice Command", sim1) # print out command
    sim1.run()  # run the Ngspice simulation
    return "done"


# endregion


def main() -> None:
    initialize(TOML_FILENAME, PROJ_NAME)
    # finished: str = simulate(ngspice_exe, proj_path / "netlists/top1.cir")
    # print(finished)


if __name__ == "__main__":
    main()
