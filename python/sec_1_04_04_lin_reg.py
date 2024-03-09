"""Example from Power Supply book: Section 1.04.04 Linear Regulator"""

# region imports
import tomllib
from pathlib import Path
from typing import Any

import py4spice as spi

# endregion


# region important constants for reading config file

# This constant is changed for each project. It matches the section name in the
# config file. It is used to decode the config file and to create the paths
MY_PROJECT: str = "sec_1_04_04"

# These are keys for the config_file_decoding. They are referenced in other parts
# of the code. They are global variables
CONFIG_NAME: str = "config_name"
GLOBAL_SECTION: str = "global_section"
NGSPICE_EXE_KEY: str = "ngspice_exe_key"
NETLISTS_DIR_KEY: str = "netlists_dir_key"
RESULTS_DIR_KEY: str = "results_dir_key"
PROJ_PATH_KEY: str = "proj_path_key"
PROJ_SECTION: str = "proj_section"

# Dictionary for decoding the config file. Do not change values unless changing the
# section or key names in the config file.
config_file_decoding: dict[str, str] = {
    CONFIG_NAME: "/workspaces/sw_pwr_book_sim/python/config.toml",
    GLOBAL_SECTION: "global",
    NGSPICE_EXE_KEY: "ngspice_exe_str",
    NETLISTS_DIR_KEY: "netlists_dir_str",
    RESULTS_DIR_KEY: "results_dir_str",
    PROJ_PATH_KEY: "proj_path_str",
    PROJ_SECTION: MY_PROJECT,
}

# keys for paths dictionary
PATH_DICT_NGSPICE_EXE: str = "ngspice_exe"
PATH_DICT_PROJ: str = "proj"
PATH_DICT_RESULTS: str = "results"
PATH_DICT_NETLISTS: str = "netlists"
# endregion


# region initialize
def define_paths(
    my_config: dict[str, Any], config_decoding: dict[str, str]
) -> tuple[Path, Path, Path, Path]:
    """Define all the paths needed for the project
    based on the project path"""

    # Here are the decodings for the config dictionary, which is from the config file
    config_global_section: str = config_decoding[GLOBAL_SECTION]
    config_ngspice_exe_key: str = config_decoding[NGSPICE_EXE_KEY]
    config_netlists_dir_key: str = config_decoding[NETLISTS_DIR_KEY]
    config_results_dir_key: str = config_decoding[RESULTS_DIR_KEY]
    config_proj_path_key: str = config_decoding[PROJ_PATH_KEY]
    config_proj_section: str = config_decoding[PROJ_SECTION]

    # # Create dictionary of paths, starting with ngspice_exe a
    # paths: dict[str, Path] = {
    #     PATH_DICT_NGSPICE_EXE: Path(
    #         my_config[config_global_section][config_ngspice_exe_key]
    #     )
    # }

    # Create dictionary of paths, starting with ngspice_exe a
    ngspice_exe: Path = my_config[config_global_section][config_ngspice_exe_key]
    proj_path: Path = Path(my_config[config_proj_section][config_proj_path_key])
    netlists_path: Path = (
        proj_path / my_config[config_global_section][config_netlists_dir_key]
    )
    results_path: Path = (
        proj_path / my_config[config_global_section][config_results_dir_key]
    )

    # # Create project path and add to dictionary
    # proj_path: Path = Path(my_config[config_proj_section][config_proj_path_key])
    # paths[PATH_DICT_PROJ] = proj_path  # Add to dictionary

    # # Create netlists directory and files if they don't exist
    # netlists_path: Path = (
    #     proj_path / my_config[config_global_section][config_netlists_dir_key]
    # )
    # netlists_path.mkdir(parents=True, exist_ok=True)  # Create the directory
    # paths[PATH_DICT_NETLISTS] = netlists_path  # Add to dictionary

    # # Create sim_results directory if doesn't exist
    # results_path: Path = (
    #     proj_path / my_config[config_global_section][config_results_dir_key]
    # )
    # results_path.mkdir(parents=True, exist_ok=True)
    # paths[PATH_DICT_RESULTS] = results_path  # Add to dictionary

    return ngspice_exe, proj_path, netlists_path, results_path


def define_vector_sets() -> tuple[spi.Vectors, spi.Vectors]:
    """Define all the vector sets for simulation and post-simulation analysis

    Returns:
        tuple[spi.Vectors, spi.Vectors]: tuple of all the vector sets defined here
    """
    vec_all = spi.Vectors("all")
    vec_in_out = spi.Vectors("in out")
    return vec_all, vec_in_out


def initialize(config_decoding: dict[str, str]) -> None:
    """stuff"""
    # read config file and create CONFIG dictionary
    config_name: Path = Path(config_decoding[CONFIG_NAME])
    with open(config_name, "rb") as file:
        my_config: dict[str, Any] = tomllib.load(file)

    # # create dictionary of paths
    # my_paths: dict[str, Path] = define_paths(my_config, config_decoding)

    ngspice_exe1, proj_path, netlists_path, results_path = define_paths(
        my_config, config_decoding
    )

    vec_all, vec_in_out = define_vector_sets()


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
    initialize(config_file_decoding)
    # finished: str = simulate(ngspice_exe, proj_path / "netlists/top1.cir")
    # print(finished)


if __name__ == "__main__":
    main()
