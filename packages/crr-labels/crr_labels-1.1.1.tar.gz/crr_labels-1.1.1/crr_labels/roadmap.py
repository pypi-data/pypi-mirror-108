from typing import List, Tuple, Union, Dict
import warnings
import pandas as pd
import compress_json
from encodeproject import download
from tqdm.auto import tqdm

from .utils import (center_window, filter_required_cell_lines,
                    normalize_bed_file, normalize_cell_lines,
                    validate_common_parameters)


def roadmap_available_cell_lines(root: str) -> pd.DataFrame:
    """Return Roadmap supported available cell lines.

    Parameters
    ---------------------------------------
    root: str,
        Where to store / load from the downloaded data.

    Returns
    ---------------------------------------
    Return dataframe with the cell lines supported available in Roadmap dataset.
    """
    info = compress_json.local_load("roadmap.json")
    filename = f"{root}/cell_lines.tsv"
    download(info["cell_lines"], filename, cache=True)
    cell_lines_codes = pd.read_csv(
        filename,
        sep="\t"
    )
    cell_lines_codes = cell_lines_codes[
        (cell_lines_codes.TYPE != "ESCDerived") & cell_lines_codes.GROUP.isin(
            ["ENCODE2012", "ESC", "IMR90"])
    ]
    cell_lines_codes["cell_line"] = cell_lines_codes.MNEMONIC.str.split(
        ".").str[1].str.replace("-", "")
    cell_lines_codes["code"] = cell_lines_codes.EID
    return cell_lines_codes[["cell_line", "code"]].reset_index(drop=True)


def filter_cell_lines(root: str, cell_lines: List[str]) -> pd.DataFrame:
    """Return Roadmap cell lines names for given cell lines.

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
    Return dataframe with the cell lines mapped to Roadmap name.
    """
    return filter_required_cell_lines(cell_lines, roadmap_available_cell_lines(root))


def get_cell_line(
    root: str,
    cell_line: str,
    states: int,
    genome: str,
    enhancers_labels: List[str],
    promoters_labels: List[str],
    url: str,
    nrows: int
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return enhancers and promoters for given cell line.

    Parameters
    -----------------------------------
    cell_line: str,
        The chosen cell line standard name.
    states: int,
        The number of states of the chosen model.
    enhancers_labels: List[str],
        The labels to use for active enhancers.
    promoters_labels: List[str],
        The labels to use for active promoters.
    url: str
        Url for downloading the chosen cell line.
    nrows: int,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Returns
    ------------------------------------
    Return tuple containing the dataframe of the enhancers
    and the dataframe of the promoters for the given cell line.
    """
    path = f"{root}/{genome}/{states}/{cell_line}.bed.gz"
    try:
        download(url, path, cache=True)
    except ValueError:
        warnings.warn(
            "Unable to retrieve the data relative to cell line {}".format(
                cell_line
            ),
            UserWarning
        )
        return None, None

    roadmap_data = pd.read_csv(
        path,
        sep="\t",
        skiprows=[0, 1],
        header=None,
        names=["chrom", "start", "end", cell_line],
        nrows=nrows
    )

    roadmap_data = roadmap_data.set_index(["chrom", "start", "end"])

    enhancers = roadmap_data[roadmap_data[cell_line].isin(
        enhancers_labels)].copy()
    promoters = roadmap_data[roadmap_data[cell_line].isin(
        promoters_labels)].copy()
    enhancers[cell_line] = 1  # Encode active enhancers as 1
    promoters[cell_line] = 1  # Encode active promoters as 1

    return enhancers, promoters


def roadmap(
    cell_lines: Union[List[str], str],
    window_size: int,
    genome: str = "hg19",
    root: str = "roadmap",
    states: int = 18,
    enhancers_labels: List[str] = ("7_Enh", "9_EnhA1", "10_EnhA2"),
    promoters_labels: List[str] = ("1_TssA",),
    nrows: int = None
):
    """Runs the pipeline over the roadmap raw data.

    Parameters
    -----------------------------
    cell_lines: List[str],
        List of cell lines to be considered.
    window_size: int,
        Window size to use for the various regions.
    genome: str= "hg19",
        Considered genome version. Currently supported only "hg19".
    states: int = 18,
        Number of the states of the model to consider. Currently supported only "15" and "18".
    enhancers_labels: List[str] = ("7_Enh", "9_EnhA1", "10_EnhA2"),
        Labels to encode as active enhancers.
    promoters_labels: List[str] = ("1_TssA",),
        Labels to enode as active promoters
    nrows:int=None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Raises
    -------------------------------
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
        If the model with *states* states is not currently supported with given genome *genome*.

    Returns
    -------------------------------
    Tuple containining dataframes informations for enhancers and promoters for chosen cell lines.
    """

    info = compress_json.local_load("roadmap.json")
    validate_common_parameters(cell_lines, [window_size], genome, info)
    cell_lines = normalize_cell_lines(cell_lines)
    if str(states) not in info[genome]["states_model"]:
        raise ValueError("The model with {states} states is not currently supported with given genome {genome}.".format(
            states=states,
            genome=genome
        ))

    cell_lines_names = filter_cell_lines(
        root,
        cell_lines,
    )

    url = info[genome]["states_model"][str(states)]
    enhancers_list, promoters_list = list(zip(*[
        (enhancers, promoters)
        for cell_line, code in tqdm(
            cell_lines_names.values,
            desc="Cell lines"
        )
        for enhancers, promoters in (get_cell_line(
            root,
            cell_line,
            states,
            genome,
            enhancers_labels,
            promoters_labels,
            url.format(code=code),
            nrows
        ),)
        if enhancers is not None and promoters is not None
    ]))
    enhancers = pd.concat(enhancers_list, axis=1).fillna(
        0
    ).astype(int)  # Encode inactive enhancers as zeros
    promoters = pd.concat(promoters_list, axis=1).fillna(
        0
    ).astype(int)  # Encode inactive promoters as zeros

    # Adapt to given window size
    enhancers = enhancers.reset_index()
    promoters = promoters.reset_index()
    enhancers = center_window(enhancers, window_size)
    promoters = center_window(promoters, window_size)

    enhancers = normalize_bed_file(cell_lines, enhancers)
    promoters = normalize_bed_file(cell_lines, promoters)

    return enhancers, promoters
