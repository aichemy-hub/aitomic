import tempfile

import polars as pl


def nmr_peaks_df_1d(zip_file: bytes) -> pl.DataFrame:
    """Exctact peaks from a zip of multiple Bruker NMR spectra.

    Examples:
        * :ref:`Getting an NMR peak data frame <getting-peak-df>`

    Parameters:
        zip_file: The content zip file containing Bruker data.

    Returns:
        The peaks as a polars data frame.

    """
    pass
