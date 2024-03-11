"""From Power Supply book: Section 1.04.04 Linear Regulator"""

# region Imports
import tomllib
from pathlib import Path
from typing import Any, Type

import py4spice as spi

# endregion


# region Constants

# This constant is set for each project. It matches the section name in the
# config file (toml). It is used to decode the config file and to create the paths
MY_PROJECT: str = "sec_1_04_04"


class Key:
    """Keys for dictionaries"""

    # Keys for decoding the config file
    CONFIG_NAME = "config_name"
    GLOBAL_SECTION = "global_section"
    NGSPICE_EXE_KEY = "ngspice_exe_str"
    NETLISTS_DIR_KEY = "netlists_dir_str"
    RESULTS_DIR_KEY = "results_dir_str"
    PROJ_PATH_KEY = "proj_path_str"
    DESCRIPTION_KEY = "description"
    PROJ_SECTION = "proj_section"

    # Keys for the paths_dict
    NGSPICE_EXE = "ngspice_exe"
    PROJ_PATH = "proj_path"
    NETLISTS_PATH = "netlists_path"
    RESULTS_PATH = "results_path"

    # Keys for the netlists_dict
    BLANKLINE = "blankline"
    TITLE = "title"
    END_LINE = "end_line"
    LOAD1 = "load1"
    LOAD2 = "load2"
    LOAD3 = "load3"
    STIMULUS1 = "stimulus1"
    STIMULUS2 = "stimulus2"
    STIMULUS3 = "stimulus3"
    SUPPLIES = "supplies"
    MODELS = "models"

    # Keys for the vectors_dict
    VEC_ALL = "vec_all"
    VEC_IN_OUT = "vec_in_out"
    VEC_OUT = "vec_out"


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
    my_config: dict[Any, Any], config_decoding: dict[str, str], Key: Type[Key]
) -> dict[str, Path]:
    """Define all the paths needed for the project"""

    # Here are the decodings for the config dictionary, which is from the config file
    config_global_section: str = config_decoding[Key.GLOBAL_SECTION]
    config_ngspice_exe_key: str = config_decoding[Key.NGSPICE_EXE_KEY]
    config_netlists_dir_key: str = config_decoding[Key.NETLISTS_DIR_KEY]
    config_results_dir_key: str = config_decoding[Key.RESULTS_DIR_KEY]
    config_proj_path_key: str = config_decoding[Key.PROJ_PATH_KEY]
    config_proj_section: str = config_decoding[Key.PROJ_SECTION]

    # Create paths based on the config dictionary
    ngspice_exe: Path = Path(my_config[config_global_section][config_ngspice_exe_key])
    proj_path: Path = Path(my_config[config_proj_section][config_proj_path_key])
    netlists_path: Path = (
        proj_path / my_config[config_global_section][config_netlists_dir_key]
    )
    results_path: Path = (
        proj_path / my_config[config_global_section][config_results_dir_key]
    )

    # create and return the paths dictionary
    return {
        Key.NGSPICE_EXE: ngspice_exe,
        Key.PROJ_PATH: proj_path,
        Key.NETLISTS_PATH: netlists_path,
        Key.RESULTS_PATH: results_path,
    }


def special_netlists(
    netlist_dict: dict[str, spi.Netlist], proj_description: str, Key: Type[Key]
) -> dict[str, spi.Netlist]:
    """Create special netlist objects and add to netlist dictionary"""

    # create blank line for spacing and add to netlist dictionary
    netlist_dict[Key.BLANKLINE] = spi.Netlist("")

    # create title netlist object and add to netlist dictionary
    netlist_dict[Key.TITLE] = spi.Netlist(proj_description)

    # create end statement netlist object and add to netlist dictionary
    netlist_dict[Key.END_LINE] = spi.Netlist(".end")

    return netlist_dict


def netlists_from_files(
    netlist_dict: dict[str, spi.Netlist], netlist_path: Path, Key: Type[Key]
) -> dict[str, spi.Netlist]:
    """read in netlists from files and add to netlist dictionary"""

    netlist_dict[Key.LOAD1] = spi.Netlist(netlist_path / "load_resistive.cir")
    netlist_dict[Key.LOAD2] = spi.Netlist(netlist_path / "load_resistive.cir")
    netlist_dict[Key.LOAD3] = spi.Netlist(netlist_path / "load_current_pulse.cir")
    netlist_dict[Key.STIMULUS1] = spi.Netlist(netlist_path / "stimulus_15v_dc.cir")
    netlist_dict[Key.STIMULUS2] = spi.Netlist(netlist_path / "stimulus_15v_ramp.cir")
    netlist_dict[Key.STIMULUS3] = spi.Netlist(netlist_path / "stimulus_15v_dc.cir")
    netlist_dict[Key.SUPPLIES] = spi.Netlist(netlist_path / "supplies.cir")
    netlist_dict[Key.MODELS] = spi.Netlist(netlist_path / "models.cir")

    return netlist_dict


def define_netlists(
    paths_dict: dict[str, Path], Key: Type[Key], proj_description: str
) -> dict[str, spi.Netlist]:
    """Create and return dictionary of netlist objects"""

    netlists_path: Path = paths_dict[Key.NETLISTS_PATH]

    netlists_dict: dict[str, spi.Netlist] = {}  # create empty netlist dictionary
    netlists_dict = special_netlists(netlists_dict, proj_description, Key)
    netlists_dict = netlists_from_files(netlists_dict, netlists_path, Key)

    # Print keys of the dictionary
    for key in netlists_dict.keys():
        print(key)

    return netlists_dict


def define_vector_sets(Key: Type[Key]) -> dict[str, spi.Vectors]:
    """Define a dictionary vector sets for simulation and post-simulation analysis"""
    return {
        Key.VEC_ALL: spi.Vectors("all"),
        Key.VEC_IN_OUT: spi.Vectors("in out"),
        Key.VEC_OUT: spi.Vectors("out"),
    }


def initialize(
    config_decoding: dict[str, str], Key: Type[Key]
) -> tuple[dict[str, Path], dict[str, spi.Netlist], dict[str, spi.Vectors]]:
    """stuff"""
    # read config file and create CONFIG dictionary
    config_name: Path = Path(config_decoding[Key.CONFIG_NAME])
    with open(config_name, "rb") as file:
        my_config: dict[str, Any] = tomllib.load(file)

    # get the project description from config file
    proj_description: str = my_config[config_file_decoding[Key.PROJ_SECTION]][
        Key.DESCRIPTION_KEY
    ]

    # create paths dictionary
    paths_dict: dict[str, Path] = define_paths(my_config, config_decoding, Key)

    # create netlists dictionary
    netlists_dict = define_netlists(paths_dict, Key, proj_description)

    # create vector sets dictionary
    vectors_dict: dict[str, spi.Vectors] = define_vector_sets(Key)

    return paths_dict, netlists_dict, vectors_dict


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
    # Initialize
    paths_dict, netlists_dict, vectors_dict = initialize(config_file_decoding, Key)
    print(netlists_dict[Key.BLANKLINE])
    print(vectors_dict[Key.VEC_IN_OUT].list_out())

    # Simulate
    finished: str = simulate(
        paths_dict[Key.NGSPICE_EXE], paths_dict[Key.NETLISTS_PATH] / "top1.cir"
    )
    print(finished)


if __name__ == "__main__":
    main()
