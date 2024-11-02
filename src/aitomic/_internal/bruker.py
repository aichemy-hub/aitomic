import tempfile
import zipfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import nmrglue
import polars as pl


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
        with tmp.joinpath("spectra.zip").open("wb") as f:
            f.write(zip_file)
        spectra_dir = tmp / "spectra"
        zipfile.ZipFile(tmp).extractall(spectra_dir)
        ppms = []
        volumes = []
        spectra = []
        for spectrum_dir in spectra_dir.glob("*"):
            for peak in _pick_peaks(spectrum_dir, peak_threshold):
                ppms.append(peak.ppm)
                volumes.append(peak.volume)
                spectra.append(spectrum_dir.name)
        return pl.DataFrame(
            {
                "spectrum": spectra,
                "ppm": ppms,
                "volume": volumes,
            }
        )


@dataclass(slots=True, frozen=True)
class NmrPeak:
    ppm: float
    volume: float


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
