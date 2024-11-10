import tempfile
import warnings
import zipfile
from collections.abc import Iterator
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import polars as pl

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import nmrglue


def nmr_peaks_df_1d(
    zip_file: bytes,
    *,
    peak_threshold: float = 1e4,
) -> pl.DataFrame:
    """Exctact peaks from a zip of multiple Bruker NMR spectra.

    Examples:
        * :ref:`Getting an NMR peak data frame <getting-peak-df>`

    Parameters:
        zip_file: The content zip file containing Bruker data.
        peak_threshold: Minimum peak height for positive peaks.

    Returns:
        The peaks as a polars data frame.

    """
    with tempfile.TemporaryDirectory() as tmp_:
        tmp = Path(tmp_)
        zipfile.ZipFile(BytesIO(zip_file)).extractall(tmp)
        ppms = []
        volumes = []
        spectra = []
        for binary_file in tmp.glob("**/1r"):
            spectrum_dir = binary_file.parent
            spectrum_label = str(spectrum_dir.relative_to(tmp))
            for peak in _pick_peaks(spectrum_dir, peak_threshold):
                ppms.append(peak.ppm)
                volumes.append(peak.integral)
                spectra.append(spectrum_label)
        return pl.DataFrame(
            {
                "spectrum": spectra,
                "ppm": ppms,
                "integral": volumes,
            }
        )


@dataclass(slots=True, frozen=True)
class NmrPeak:
    ppm: float
    integral: float


def _pick_peaks(
    spectrum_dir: Path,
    peak_threshold: float,
) -> Iterator[NmrPeak]:
    metadata, data = nmrglue.bruker.read_pdata(str(spectrum_dir))
    udic = nmrglue.bruker.guess_udic(metadata, data)
    unit_conversion = nmrglue.fileio.fileiobase.uc_from_udic(udic)
    for peak in nmrglue.peakpick.pick(
        data, pthres=peak_threshold, nthres=None
    ):
        ppm = unit_conversion.ppm(peak["X_AXIS"])
        volume = peak["VOL"]
        yield NmrPeak(ppm, volume)
