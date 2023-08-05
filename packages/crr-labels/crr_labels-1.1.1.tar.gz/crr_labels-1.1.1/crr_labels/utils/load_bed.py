import pandas as pd


def load_bed(path: str) -> pd.DataFrame:
    """Return bed file from given path.

    Parameters
    -----------------------
    path: str,
        Path from where to load the bed file.

    Returns
    -----------------------
    Pandas dataframe with bed file informations.
    """
    return pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["chrom", "start", "end", "name", "score", "strand",
               "thickStart", "thickEnd", "itemRgb", "blockCount", "blockSizes", "blockStarts"],
        low_memory=False
    )
