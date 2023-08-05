from encodeproject import download
from .utils import filter_required_cell_lines, validate_common_parameters, center_window, normalize_cell_lines, normalize_bed_file, load_bed
from typing import List, Dict, Tuple,  Union, Generator
import compress_json
import pandas as pd


def fantom_available_cell_lines(
    root: str = "fantom",
) -> pd.DataFrame:
    """Return supported cell lines available within FANTOM dataset.

    Parameters
    ---------------------------------------
    root: str = "fantom",
        Where to store / load from the downloaded data.

    Returns
    ---------------------------------------
    Return dataframe with the supported cell lines mapped to FANTOM name.
    """
    info = compress_json.local_load("fantom.json")
    path = f"{root}/cell_lines.tsv"
    download(info["cell_lines"], path, cache=True)
    df = pd.read_csv(
        path,
        sep="\t",
        header=None
    )
    cell_lines_names = df[0].str.split("cell line:", expand=True)
    cell_lines_names[1][
        cell_lines_names[0].str.startswith("H1") &
        cell_lines_names[0].str.contains("day00")
    ] = "H1"
    cell_lines_names[1][
        cell_lines_names[0].str.startswith("H9") &
        cell_lines_names[0].str.contains("H9ES")
    ] = "H9"
    nan_mask = pd.notnull(cell_lines_names[1])
    cell_lines_names = cell_lines_names[nan_mask]
    infected_mask = ~cell_lines_names[1].str.contains("infection")
    cell_lines_names = cell_lines_names[infected_mask]
    cell_lines_names[1] = cell_lines_names[1].str.split("/").str[0]
    cell_lines_names[1] = cell_lines_names[1].str.split(",").str[0]
    cell_lines_codes = pd.concat(
        objs=[
            cell_lines_names[1].apply(lambda x: x.split("ENCODE")[
                                      0].strip()).str.upper().str.replace("-", ""),
            df[nan_mask][infected_mask][1],
        ],
        axis=1
    )
    cell_lines_codes.columns = ["cell_line", "code"]
    return cell_lines_codes.reset_index(drop=True).groupby("cell_line").first().reset_index()


def filter_cell_lines(root: str, cell_lines: List[str]) -> pd.DataFrame:
    """Return FANTOM cell lines names for given cell lines.

    Parameters
    ---------------------------------------
    root: str,
        Where to store / load from the downloaded data.
    cell_lines: List[str],
        list of cell lines to be considered.

    Raises
    ---------------------------------------
    ValueError:
        if a required cell line is not currently available.

    Returns
    ---------------------------------------
    Return dataframe with the cell lines mapped to FANTOM name.
    """
    return filter_required_cell_lines(cell_lines, fantom_available_cell_lines(root))


def average_cell_lines(cell_lines_names: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    """Return dataframe with cell line columns averaged.

    Example: for HelaS3 there are 3 experiments, the values for HelaS3 are therefore averaged.

    Parameters
    ----------------------------------
    cell_lines_names: pd.DataFrame, the dataframe with required cell lines mapping.
    data: pd.DataFrame, the data informations to be averaged.

    Returns
    ----------------------------------
    The averaged dataframe.
    """
    for cell_line, group in cell_lines_names.groupby("cell_line"):
        data[cell_line] = data[group.code].astype(
            float
        ).mean(skipna=True, axis=1)
    return data.drop(columns=data.columns[data.columns.str.startswith("CNhs")])


def load_matrix(root: str, genome: str, region: str, info: Dict, nrows: int) -> pd.DataFrame:
    """Return the matrix with the CAGE peaks data.

    Parameters
    ----------------------
    root: str,
        Root where to store the downloaded data.
    genome: str,
        Genomic assembly.
    region: str,
        Name of the regions to consider.
    info: Dict,
        URls data.
    nrows: int= None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Returns
    ----------------------
    Pandas dataframe with CAGE peaks data.
    """
    matrix_path = f"{root}/{genome}/{region}/matrix.tsv.gz"
    bed_path = f"{root}/{genome}/{region}/regions.bed.gz"
    download(info[genome][region]["matrix"], matrix_path, cache=True)
    download(info[genome][region]["bed"], bed_path, cache=True)
    if nrows is not None and region == "promoters":
        nrows += 2
    matrix = pd.read_csv(
        matrix_path,
        comment="#",
        sep="\t",
        low_memory=False,
        nrows=nrows
    )
    if region == "promoters":
        matrix.drop(index=[0, 1], inplace=True)
        matrix.reset_index(drop=True, inplace=True)
    matrix.set_index(matrix.columns[0], inplace=True)
    bed = load_bed(bed_path)
    bed.set_index("name", inplace=True)
    matrix = pd.concat(
        [
            bed.loc[matrix.index],
            matrix
        ],
        axis=1
    )
    matrix.reset_index(drop=True, inplace=True)
    return matrix


def filter_promoters(
    root: str,
    cell_lines: List[str],
    cell_lines_names: pd.DataFrame,
    genome: str,
    info: Dict,
    window_sizes: List[int],
    nrows: int
) -> Generator:
    """Return DataFrame containing the promoters filtered for given cell lines and adapted to given window size.

    Parameters
    ---------------------------------------
    root: str,
        Directory where to store / load the downloaded data.
    cell_lines: List[str],
        list of cell lines to be considered.
    cell_lines_names: pd.DataFrame,
        DataFrame containing FANTOM map from cell line name to FANTOM code.
    genome: str,
        considered genome version.
    info: Dict,
        URLs from where to retrieve the data.
    window_sizes: List[int],
        window size to use for the various regions.
    nrows:int=None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Returns
    ---------------------------------------
    DataFrame containing filtered promoters.
    """
    # Load the data matrix
    promoters = load_matrix(
        root,
        genome,
        "promoters",
        info,
        nrows
    )

    # Filter columns not relative to CAGE features
    promoters.drop(
        columns=[
            c
            for c in promoters.columns
            if c.endswith("_id")
        ],
        inplace=True
    )
    promoters.columns = [
        c.split(".")[2]
        if c.startswith("tpm") else c
        for c in promoters.columns
    ]

    # Keep only the lines relative to promoters
    promoters = promoters[promoters.description.str.endswith("end")]

    # Handle the strand-related window size.
    positive_strand = promoters.strand == "+"
    negative_strand = promoters.strand == "-"

    # For each window size required we yield the promoters
    for window_size in window_sizes:
        current = promoters.copy()
        current.loc[current.index[positive_strand],
                    "start"] = current[positive_strand]["end"] - window_size
        current.loc[current.index[negative_strand],
                    "end"] = current[negative_strand]["start"] + window_size
        yield current


def filter_enhancers(
    root: str,
    cell_lines: List[str],
    cell_lines_names: pd.DataFrame,
    genome: str,
    info: Dict,
    window_sizes: List[int],
    center_mode: str,
    nrows: int
) -> Generator:
    """Return DataFrame containing the enhancers filtered for given cell lines and adapted to given window size.

    Parameters
    ---------------------------------------
    root: str,
        Path where to store / load data.
    cell_lines: List[str],
        list of cell lines to be considered.
    cell_lines_names: pd.DataFrame,
        DataFrame containing FANTOM map from cell line name to FANTOM code.
    genome: str,
        considered genome version.
    window_sizes: List[int],
        window size to use for the various regions.
    center_enhancers: str,
        how to center the enhancer window, either around "peak" or the "center" of the region.
    threshold: float,
        activation threshold.
    binarize: bool,
        Wether to binarize the labels.
    nrows:int=None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Returns
    ---------------------------------------
    DataFrame containing filtered enhancers.
    """
    # Load the enhancers data
    enhancers = load_matrix(
        root,
        genome,
        "enhancers",
        info,
        nrows
    )
    # Center the windows for each window size.
    for window_size in window_sizes:
        yield center_window(
            enhancers.copy(),
            window_size,
            enhancers.thickStart if center_mode == "peak" else None
        )


def fantom(
    cell_lines: Union[List[str], str],
    window_sizes: Union[List[int], int],
    root: str = "fantom",
    genome: str = "hg38",
    center_enhancers: str = "peak",
    enhancers_threshold: float = 0,
    promoters_threshold: float = 5,
    binarize: bool = True,
    nrows: int = None
) -> Generator:
    """Runs the pipeline over the fantom raw CAGE data.

    Parameters
    ---------------------------------------
    cell_lines: List[str],
        list of cell lines to be considered.
    window_size: Union[List[int], int],
        Either window size or list of to use for the various regions.
    genome: str= "hg38",
        considered genome version.
    center_enhancers: str= "peak",
        how to center the enhancer window, either around "peak" or the "center" of the region.
    enhancers_threshold:float= 0,
        activation threshold for the enhancers.
    promoters_threshold:float= 5,
        activation threshold for the promoters.
    binarize: bool= True,
        Whetever to return the data binary-encoded, zero for inactive, one for active.
    nrows: int= None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Raises
    ----------------------------------------
    ValueError:
        If given cell lines list is empty.
    ValueError:
        If given cell lines are not strings.
    ValueError:
        If given window size is not an integer.
    ValueError:
        If given window size is not a strictly positive integer.
    ValueError:
        If given genome version is not a string.
    ValueError:
        If given nrows parameter is not None or a strictly positive integer.
    ValueError:
        If given thresholds are not positive real numbers.
    ValueError:
        If given center_enhancers is not "peak" or "center".

    Returns
    ----------------------------------------
    Tuple containining dataframes informations for enhancers and promoters for chosen cell lines.
    """
    if isinstance(cell_lines, str):
        cell_lines = [cell_lines]
    if isinstance(window_sizes, int):
        window_sizes = [window_sizes]

    for threshold in (enhancers_threshold, promoters_threshold):
        if not isinstance(threshold, (float, int)) or threshold < 0:
            raise ValueError("Threshold must be a positive real number.")

    if center_enhancers not in ("peak", "center"):
        raise ValueError("The given center_enhancers option {center_enhancers} is not supported.".format(
            center_enhancers=center_enhancers
        ))

    info = compress_json.local_load("fantom.json")
    validate_common_parameters(cell_lines, window_sizes, genome, info)
    cell_lines = normalize_cell_lines(cell_lines)
    cell_lines_names = filter_cell_lines(root, cell_lines)

    enhancers_generator = filter_enhancers(
        root=root,
        cell_lines=cell_lines,
        cell_lines_names=cell_lines_names,
        genome=genome,
        info=info,
        window_sizes=window_sizes,
        center_mode=center_enhancers,
        nrows=nrows
    )

    promoters_generator = filter_promoters(
        root=root,
        cell_lines=cell_lines,
        cell_lines_names=cell_lines_names,
        genome=genome,
        info=info,
        window_sizes=window_sizes,
        nrows=nrows
    )

    for enhancers, promoters in zip(enhancers_generator, promoters_generator):
        regions = []
        for crrs, threshold in (
            (enhancers, enhancers_threshold),
            (promoters, promoters_threshold),
        ):
            average_cell_lines(cell_lines_names, crrs)
            crrs = normalize_bed_file(
                cell_lines,
                crrs
            )
            if binarize:
                crrs[cell_lines] = (crrs[cell_lines] > threshold).astype(int)
            regions.append(crrs)
        yield regions
