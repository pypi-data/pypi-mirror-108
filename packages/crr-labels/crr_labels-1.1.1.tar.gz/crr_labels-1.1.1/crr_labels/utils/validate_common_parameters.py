from typing import List, Dict


def validate_common_parameters(
    cell_lines: List[str],
    window_sizes: List[int],
    genome: str,
    info: Dict
):
    """Checks for possible errors in the input parameters.

    Parameters
    -----------------------
    cell_lines: List[str],
        List of cell lines to be considered.
    window_sizes: List[int],
        Window size to use for the various regions.
    genome: str,
        Considered genome version. Currently supported only "hg19".
    nrows:int,
        The number of rows to read, usefull when testing pipelines for creating smaller datasets.
    info:Dict,
        The informations for the dataset that is currently being rendered.

    Raises
    ------------------------
    ValueError:
        If given cell lines list is empty.
    ValueError:
        If given cell lines are not strings.
    ValueError:
        If given window size is not a strictly positive integer.
    ValueError:
        If given genome version is not a string.
    ValueError:
        If given nrows parameter is not None or a strictly positive integer.
    """
    if len(cell_lines) == 0:
        raise ValueError("Given cell lines list is empty.")
    if any([
        not isinstance(cell_line, str) for cell_line in cell_lines
    ]):
        raise ValueError("Given cell lines are not strings.")
    for window_size in window_sizes:
        if window_size <= 0:
            raise ValueError(
                "Given window size is not a strictly positive integer.")
    if not isinstance(genome, str):
        raise ValueError("Given genome version is not a string.")
    if genome not in info:
        raise ValueError("Given genome {genome} is not currently supported.".format(
            genome=genome
        ))
