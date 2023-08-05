from typing import List


def normalize_cell_lines(cell_lines: List[str]) -> List[str]:
    """Return normalized cell lines.

    Currently, the only normalization procedure is to convert the cell lines
    to uppercase.

    Parameters
    ----------------------
    cell_lines: List[str],
        The list of the cell lines.

    Returns
    ----------------------
    List of the normalized cell line names.
    """
    return [
        cell_line.upper()
        for cell_line in cell_lines
    ]
