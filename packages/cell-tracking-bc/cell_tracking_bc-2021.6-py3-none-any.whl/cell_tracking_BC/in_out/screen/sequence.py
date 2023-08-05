# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Sequence

import matplotlib.pyplot as pypl
import numpy as nmpy
import scipy.interpolate as ntrp
import skimage.measure as msre
from cell_tracking_BC.in_out.storage.archiver import archiver_t
from cell_tracking_BC.type.sequence import sequence_t
from matplotlib.widgets import Slider as slider_t
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t


array_t = nmpy.ndarray


def ShowSegmentation(
    sequence: sequence_t,
    /,
    *,
    which_compartment: str = None,
    as_3d: bool = False,
    time_offset_factor: float = 1.0,
    as_tunnels: bool = False,
    tunnel_time_steps: int = 100,
    show_and_wait: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> None:
    """
    which_compartment: "nucleus" or "cytoplasm" or "cell" or None. If None, then the first non-None in the order "cell",
    "cytoplasm", "nucleus" is selected.
    """
    if which_compartment == "nucleus":
        segmentations = sequence.nuclei_sgms
    elif which_compartment == "cytoplasm":
        segmentations = sequence.cytoplasms_sgms
    elif which_compartment == "cell":
        segmentations = sequence.cells_sgms
    elif which_compartment is None:
        if sequence.cells_sgms is not None:
            segmentations = sequence.cells_sgms
        elif sequence.cytoplasms_sgms is not None:
            segmentations = sequence.cytoplasms_sgms
        elif sequence.nuclei_sgms is not None:
            segmentations = sequence.nuclei_sgms
        else:
            raise RuntimeError("No segmentations computed yet")
    else:
        raise ValueError(f"{which_compartment}: Invalid compartment designation")

    figure = pypl.figure()

    if as_3d or as_tunnels:
        axes = figure.add_subplot(projection=axes_3d_t.name)
        axes.set_xlabel("row positions")
        axes.set_ylabel("column positions")
        axes.set_zlabel("time points")

        if as_tunnels:
            _ShowSegmentationAsTunnels(segmentations, tunnel_time_steps, axes)
        else:
            _ShowSegmentationAsMilleFeuille(segmentations, time_offset_factor, axes)
    else:
        axes = figure.add_subplot(111)
        _ = _ShowSegmentationAsSequence(segmentations, figure, axes)

    _FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


def _ShowSegmentationAsTunnels(
    segmentations: Sequence[array_t], tunnel_time_steps: int, axes: axes_3d_t
) -> None:
    """"""
    volume = nmpy.array(segmentations)
    original_extents = (
        range(volume.shape[0]),
        range(volume.shape[1]),
        range(volume.shape[2]),
    )
    interpolated_extents = (
        nmpy.linspace(0, volume.shape[0] - 1, num=tunnel_time_steps),
        *original_extents[1:],
    )
    all_times, all_rows, all_cols = nmpy.meshgrid(*interpolated_extents, indexing="ij")
    interpolated_sites = nmpy.vstack((all_times.flat, all_rows.flat, all_cols.flat)).T
    interpolated = ntrp.interpn(original_extents, volume, interpolated_sites)
    reshaped = nmpy.reshape(
        interpolated, (interpolated_extents[0].size, *volume.shape[1:])
    )
    reorganized = nmpy.moveaxis(reshaped, (0, 1, 2), (2, 0, 1))
    vertices, faces, *_ = msre.marching_cubes(reorganized, 0.5, step_size=5)
    axes.plot_trisurf(
        vertices[:, 0],
        vertices[:, 1],
        faces,
        vertices[:, 2],
        cmap="Spectral",
        lw=1,
    )


def _ShowSegmentationAsMilleFeuille(
    segmentations: Sequence[array_t], time_offset_factor: float, axes: axes_3d_t
) -> None:
    """"""
    shape = segmentations[0].shape
    all_rows, all_cols = nmpy.meshgrid(range(shape[0]), range(shape[1]), indexing="ij")
    for t_idx, segmentation in enumerate(segmentations):
        axes.contourf(
            all_rows,
            all_cols,
            segmentation,
            levels=1,
            zdir="z",
            offset=time_offset_factor * t_idx,
            alpha=0.8,
            cmap="gray",
        )
    axes.set_zlim(0, time_offset_factor * (segmentations.__len__() - 1))


def _ShowSegmentationAsSequence(
    segmentations: Sequence[array_t], figure: pypl.Figure, axes: pypl.Axes
) -> slider_t:
    """
    Returns the slider so that a reference can be kept in calling function to maintain it responsive
    """
    axes.matshow(segmentations[0], cmap="gray")

    figure.subplots_adjust(bottom=0.25)
    slider_axes = figure.add_axes([0.25, 0.15, 0.65, 0.03])
    slider = slider_t(
        slider_axes,
        "Time Point",
        0,
        segmentations.__len__() - 1,
        valinit=0,
        valstep=1,
    )

    def OnNewSliderValue(value: float, /) -> None:
        time_point = int(round(value))
        axes.matshow(segmentations[time_point], cmap="gray")
        figure.canvas.draw_idle()

    slider.on_changed(OnNewSliderValue)

    return slider


def ShowTracking(
    sequence: sequence_t,
    /,
    *,
    show_and_wait: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> None:
    """"""
    figure = pypl.figure()
    axes = figure.add_subplot(projection=axes_3d_t.name)
    axes.set_xlabel("row positions")
    axes.set_ylabel("column positions")
    axes.set_zlabel("time points")

    colors = "bgrcmyk"

    for t_idx, track in enumerate(sequence.TracksIterator()):
        color_idx = t_idx % colors.__len__()

        for time_point, src_cell, tgt_cell in track.SegmentsIterator():
            time_points = (time_point, time_point + 1)
            rows = (src_cell.centroid[0], tgt_cell.centroid[0])
            cols = (src_cell.centroid[1], tgt_cell.centroid[1])
            axes.plot3D(rows, cols, time_points, colors[color_idx])

    _FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


def _FinalizeDisplay(
    figure: pypl.Figure, figure_name: str, show_and_wait: bool, archiver: archiver_t
) -> None:
    """"""
    if archiver is not None:
        figure.canvas.draw_idle()
        archiver.Store(figure, figure_name)

    if show_and_wait:
        pypl.show()
