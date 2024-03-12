"""From Power Supply book: Section 1.04.04 Linear Regulator"""

# region Imports
import tomllib
from pathlib import Path
from typing import Any

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
    DUT = "dut"
    CONTROL1 = "control1"
    TOP1 = "top1"

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


# region functions
def define_paths(
    my_config: dict[Any, Any], config_decoding: dict[str, str]
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

    # create results directory if it does not exist
    results_path.mkdir(parents=True, exist_ok=True)

    # create and return the paths dictionary
    return {
        Key.NGSPICE_EXE: ngspice_exe,
        Key.PROJ_PATH: proj_path,
        Key.NETLISTS_PATH: netlists_path,
        Key.RESULTS_PATH: results_path,
    }


def special_netlists(
    netlists_dict: dict[str, spi.Netlist], proj_description: str
) -> dict[str, spi.Netlist]:
    """Create special netlist objects and add to netlist dictionary"""

    # create blank line for spacing and add to netlist dictionary
    netlists_dict[Key.BLANKLINE] = spi.Netlist("")

    # create title netlist object and add to netlist dictionary
    netlists_dict[Key.TITLE] = spi.Netlist(f"* {proj_description}")

    # create end statement netlist object and add to netlist dictionary
    netlists_dict[Key.END_LINE] = spi.Netlist(".end")

    return netlists_dict


def netlists_from_files(
    netlists_dict: dict[str, spi.Netlist], netlist_path: Path
) -> dict[str, spi.Netlist]:
    """read in netlists from files and add to netlist dictionary"""

    netlists_dict[Key.LOAD1] = spi.Netlist(netlist_path / "load_resistive.cir")
    netlists_dict[Key.LOAD2] = spi.Netlist(netlist_path / "load_resistive.cir")
    netlists_dict[Key.LOAD3] = spi.Netlist(netlist_path / "load_current_pulse.cir")
    netlists_dict[Key.STIMULUS1] = spi.Netlist(netlist_path / "stimulus_15v_dc.cir")
    netlists_dict[Key.STIMULUS2] = spi.Netlist(netlist_path / "stimulus_15v_ramp.cir")
    netlists_dict[Key.STIMULUS3] = spi.Netlist(netlist_path / "stimulus_15v_dc.cir")
    netlists_dict[Key.SUPPLIES] = spi.Netlist(netlist_path / "supplies.cir")
    netlists_dict[Key.MODELS] = spi.Netlist(netlist_path / "models.cir")

    return netlists_dict


def prepare_dut(
    netlists_dict: dict[str, spi.Netlist], netlists_path: Path
) -> dict[str, spi.Netlist]:
    """Prepare dut.cir from raw_kicad.cir"""

    dut: spi.Netlist = spi.Netlist(netlists_path / "raw_kicad.cir")
    dut.del_line_starts_with(".title")  # delete first line (title)
    dut.del_line_starts_with(".end")  # delete last line (.end)
    dut.del_line_starts_with(".include")  # delete first  .include line
    dut.del_line_starts_with(".include")  # delete second .include line
    dut.del_slash()  # delete forward slashes from node names

    netlists_dict[Key.DUT] = dut  # add to netlist dictionary

    return netlists_dict


def define_netlists(
    paths_dict: dict[str, Path], proj_description: str
) -> dict[str, spi.Netlist]:
    """Create and return dictionary of netlist objects"""

    netlists_path: Path = paths_dict[Key.NETLISTS_PATH]

    netlists_dict: dict[str, spi.Netlist] = {}  # create empty netlist dictionary
    netlists_dict = special_netlists(netlists_dict, proj_description)
    netlists_dict = netlists_from_files(netlists_dict, netlists_path)
    netlists_dict = prepare_dut(netlists_dict, netlists_path)

    return netlists_dict


def define_vector_sets() -> dict[str, spi.Vectors]:
    """Define a dictionary vector sets for simulation and post-simulation analysis"""
    return {
        Key.VEC_ALL: spi.Vectors("all"),
        Key.VEC_IN_OUT: spi.Vectors("in out"),
        Key.VEC_OUT: spi.Vectors("out"),
    }


def initialize(
    config_decoding: dict[str, str]
) -> tuple[dict[str, Path], dict[str, spi.Netlist], dict[str, spi.Vectors]]:
    """Initialize the project by creating paths, netlists, and vector sets"""
    # read config file and create CONFIG dictionary
    config_name: Path = Path(config_decoding[Key.CONFIG_NAME])
    with open(config_name, "rb") as file:
        my_config: dict[str, Any] = tomllib.load(file)

    # get the project description from config file
    proj_description: str = my_config[config_file_decoding[Key.PROJ_SECTION]][
        Key.DESCRIPTION_KEY
    ]

    # create paths dictionary
    paths_dict: dict[str, Path] = define_paths(my_config, config_decoding)

    # create netlists dictionary
    netlists_dict = define_netlists(paths_dict, proj_description)

    # create vector sets dictionary
    vectors_dict: dict[str, spi.Vectors] = define_vector_sets()

    return paths_dict, netlists_dict, vectors_dict


def define_analyses(
    paths_dict: dict[str, Path], vectors_dict: dict[str, spi.Vectors]
) -> list[spi.Analyses]:
    """Define and return a list of analyses"""

    # vectors for each analysis and path to put results
    vec_all: spi.Vectors = vectors_dict[Key.VEC_ALL]
    results_path: Path = paths_dict[Key.RESULTS_PATH]

    # create empty list. Next sections define
    list_of_analyses1: list[spi.Analyses] = []

    # 1st analysis: operating point
    op_cmd = "op"
    op1 = spi.Analyses("op1", "op", op_cmd, vec_all, results_path)
    list_of_analyses1.append(op1)

    # 2nd analysis: transfer function
    tf_cmd = "tf v(out) vin"
    tf1 = spi.Analyses("tf1", "tf", tf_cmd, vec_all, results_path)
    list_of_analyses1.append(tf1)

    return list_of_analyses1


def create_control_section(list_of_analyses1: list[spi.Analyses]) -> spi.Netlist:

    my_control1 = spi.Control()  # create 'my_control' object
    my_control1.insert_lines(["listing"])  # cmd to list out netlist
    for analysis in list_of_analyses1:  # statements for all analyses
        my_control1.insert_lines(analysis.lines_for_cntl())
    control1: spi.Netlist = spi.Netlist(str(my_control1))  # create netlist object

    return control1


def create_top1_netlist(
    netlists_dict: dict[str, spi.Netlist]
) -> dict[str, spi.Netlist]:
    """Create top1 netlist object and add to netlist dictionary"""

    # concatenate all tne netlists to make top1 and add to netlist dict
    netlists_dict[Key.TOP1] = (
        netlists_dict[Key.TITLE]
        + netlists_dict[Key.BLANKLINE]
        + netlists_dict[Key.DUT]
        + netlists_dict[Key.LOAD1]
        + netlists_dict[Key.BLANKLINE]
        + netlists_dict[Key.SUPPLIES]
        + netlists_dict[Key.BLANKLINE]
        + netlists_dict[Key.STIMULUS1]
        + netlists_dict[Key.BLANKLINE]
        + netlists_dict[Key.MODELS]
        + netlists_dict[Key.BLANKLINE]
        + netlists_dict[Key.CONTROL1]
        + netlists_dict[Key.END_LINE]
    )
    return netlists_dict


def execute_ngspice(ngspice_exe: Path, netlist: Path) -> str:
    """Execute ngspice and return 'done' when finished"""

    # prepare simulate object, print out command, and simulate
    sim1: spi.Simulate = spi.Simulate(ngspice_exe, netlist)
    # spi.print_section("Ngspice Command", sim1) # print out command
    sim1.run()  # run the Ngspice simulation
    return "done"


def convert_to_numpy(list_of_analyses: list[spi.Analyses]) -> list[spi.SimResults]:
    # convert the raw results into list of SimResults objects
    return [
        spi.SimResults.from_file(analysis.cmd_type, analysis.results_filename)
        for analysis in list_of_analyses
    ]


def simulate(
    paths_dict: dict[str, Path],
    netlists_dict: dict[str, spi.Netlist],
    list_of_analyses: list[spi.Analyses],
) -> tuple[list[spi.SimResults], dict[str, spi.Netlist]]:

    # create control section and add to netlist dictionary
    netlists_dict[Key.CONTROL1] = create_control_section(list_of_analyses)

    # create top1 netlist object and add to netlist dictionary
    netlists_dict = create_top1_netlist(netlists_dict)

    # write top1 netlist to file
    top1_file: Path = paths_dict[Key.NETLISTS_PATH] / "top1.cir"
    netlists_dict[Key.TOP1].write_to_file(top1_file)

    # execute ngspice
    finished: str = execute_ngspice(paths_dict[Key.NGSPICE_EXE], top1_file)
    print(finished)

    # create empty list for simulation results
    sim_results: list[spi.SimResults] = convert_to_numpy(list_of_analyses)

    return sim_results, netlists_dict


def analyze_results(
    sim_results: list[spi.SimResults], vectors_dict: dict[str, spi.Vectors]
) -> None:
    # give each SimResults object a more descriptive name
    op1_results, tf1_results = sim_results

    # diaplay results for operating point analysis
    spi.print_section("Operating Point Results", op1_results.print_table())

    # display results for small signal transfer function analysis
    spi.print_section("Transfer Function Results", tf1_results.print_table())


# endregion


def main() -> None:
    # Initialize
    paths_dict, netlists_dict, vectors_dict = initialize(config_file_decoding)

    # Define analyses
    list_of_analyses: list[spi.Analyses] = define_analyses(paths_dict, vectors_dict)

    # Simulate
    sim_results, netlists_dict = simulate(paths_dict, netlists_dict, list_of_analyses)

    analyze_results(sim_results, vectors_dict)


if __name__ == "__main__":
    main()
