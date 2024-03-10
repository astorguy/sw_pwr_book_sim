"""Example from Power Supply book: Section 1.04.04 Linear Regulator"""

# region Imports
import tomllib
from pathlib import Path
from typing import Any

import py4spice as spi

# endregion


# region Important constants for reading config file

# This constant is changed for each project. It matches the section name in the
# config file. It is used to decode the config file and to create the paths
MY_PROJECT: str = "sec_1_04_04"


class Key:
    """Keys for dictionaries"""

    CONFIG_NAME = "config_name"
    GLOBAL_SECTION = "global_section"
    NGSPICE_EXE_KEY = "ngspice_exe_str"
    NETLISTS_DIR_KEY = "netlists_dir_str"
    RESULTS_DIR_KEY = "results_dir_str"
    PROJ_PATH_KEY = "proj_path_str"
    PROJ_SECTION = "proj_section"


# Dictionary for decoding the config file. Do not change values unless changing the
# section or key names in the config file.
config_file_decoding = {
    Key.CONFIG_NAME: "/workspaces/sw_pwr_book_sim/python/config.toml",
    Key.GLOBAL_SECTION: "global",
    Key.NGSPICE_EXE_KEY: "ngspice_exe_str",
    Key.NETLISTS_DIR_KEY: "netlists_dir_str",
    Key.RESULTS_DIR_KEY: "results_dir_str",
    Key.PROJ_PATH_KEY: "proj_path_str",
    Key.PROJ_SECTION: MY_PROJECT,
}
# endregion


# region Initialize
def define_paths(
    my_config: dict[str, str], config_decoding: dict[str, str]
) -> tuple[Path, Path, Path, Path]:
    """Define all the paths needed for the project"""

    # Here are the decodings for the config dictionary, which is from the config file
    config_global_section: str = config_decoding[Key.GLOBAL_SECTION]
    config_ngspice_exe_key: str = config_decoding[Key.NGSPICE_EXE_KEY]
    config_netlists_dir_key: str = config_decoding[Key.NETLISTS_DIR_KEY]
    config_results_dir_key: str = config_decoding[Key.RESULTS_DIR_KEY]
    config_proj_path_key: str = config_decoding[Key.PROJ_PATH_KEY]
    config_proj_section: str = config_decoding[Key.PROJ_SECTION]

    # Create paths based on the config dictionary
    fred: str = my_config["global"]["ngspice_exe_str"]
    print(f"fred = {fred}")
    ngspice_exe: Path = Path(my_config[config_global_section][config_ngspice_exe_key])
    proj_path: Path = Path(my_config[config_proj_section][config_proj_path_key])
    netlists_path: Path = (
        proj_path / my_config[config_global_section][config_netlists_dir_key]
    )
    results_path: Path = (
        proj_path / my_config[config_global_section][config_results_dir_key]
    )

    return ngspice_exe, proj_path, netlists_path, results_path


def define_vector_sets() -> tuple[spi.Vectors, spi.Vectors]:
    """Define all the vector sets for simulation and post-simulation analysis

    Returns:
        tuple[spi.Vectors, spi.Vectors]: tuple of all the vector sets defined here
    """
    vec_all = spi.Vectors("all")
    vec_in_out = spi.Vectors("in out")
    return vec_all, vec_in_out


def define_netlists(netlists_path: Path) -> None:
    print(netlists_path)


def initialize(config_decoding: dict[str, str]) -> None:
    """stuff"""
    # read config file and create CONFIG dictionary
    config_name: Path = Path(config_decoding[Key.CONFIG_NAME])
    with open(config_name, "rb") as file:
        my_config: dict[str, Any] = tomllib.load(file)

    # define all the paths
    ngspice_exe, proj_path, netlists_path, results_path = define_paths(
        my_config, config_decoding
    )

    # # define all the vector sets
    # vec_all, vec_in_out = define_vector_sets()

    # # create netlist objects
    # define_netlists(netlists_path)


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
    print("hello")
    initialize(config_file_decoding)
    # finished: str = simulate(ngspice_exe, proj_path / "netlists/top1.cir")
    # print(finished)


if __name__ == "__main__":
    main()
