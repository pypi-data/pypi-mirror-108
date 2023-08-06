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
import matplotlib.text as text
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
    with_labels: bool = True,
    mode: str = "2d+t",
    time_stretching: float = 1.0,
    show_and_wait: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> None:
    """
    which_compartment: "nucleus" or "cytoplasm" or "cell" or None. If None, then the first non-None in the order "cell",
    "cytoplasm", "nucleus" is selected.
    mode: "2d+t", "mille-feuille", "tunnels"
    time_stretching: must be >= 1.0
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

    if mode == "2d+t":
        axes = figure.add_subplot(111)
        # Maintain a reference to the slider so that it remains functional
        figure.__SEQUENCE_SLIDER_REFERENCE__ = _ShowSegmentationsAs2DpT(
            segmentations, with_labels, figure, axes
        )
    elif mode in ("mille-feuille", "tunnels"):
        axes = figure.add_subplot(projection=axes_3d_t.name)
        axes.set_xlabel("row positions")
        axes.set_ylabel("column positions")
        axes.set_zlabel("time points")

        if mode == "mille-feuille":
            _ShowSegmentationsAsMilleFeuille(
                segmentations, with_labels, time_stretching, axes
            )
        else:
            _ShowSegmentationsAsTunnels(segmentations, time_stretching, axes)
    else:
        raise ValueError(
            f'{mode}: Invalid mode; Expected="2d+t", "mille-feuille", "tunnels"'
        )

    _FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


def _ShowSegmentationsAs2DpT(
    segmentations: Sequence[array_t],
    with_labels: bool,
    figure: pypl.Figure,
    axes: pypl.Axes,
    /,
) -> slider_t:
    """
    Returns the slider so that a reference can be kept in calling function to maintain it responsive
    """
    _ShowSegmentation(segmentations[0], with_labels, axes)

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
        _ShowSegmentation(segmentations[time_point], with_labels, axes)
        figure.canvas.draw_idle()

    slider.on_changed(OnNewSliderValue)

    return slider


def _ShowSegmentation(
    segmentation: array_t, with_labels: bool, axes: pypl.Axes, /
) -> None:
    """"""
    axes.matshow(segmentation, cmap="gray")
    if with_labels:
        _AnnotateCells(segmentation, axes)


def _ShowSegmentationsAsMilleFeuille(
    segmentations: Sequence[array_t],
    with_labels: bool,
    time_stretching: float,
    axes: axes_3d_t,
    /,
) -> None:
    """"""
    n_segmentations = segmentations.__len__()
    shape = segmentations[0].shape

    all_rows, all_cols = nmpy.meshgrid(range(shape[0]), range(shape[1]), indexing="ij")
    for t_idx, segmentation in enumerate(segmentations):
        axes.contourf(
            all_rows,
            all_cols,
            segmentation,
            levels=1,
            offset=time_stretching * t_idx,
            alpha=0.8,
            cmap="gray",
        )
        if with_labels:
            _AnnotateCells(
                segmentation, axes, elevation=time_stretching * (t_idx + 0.2)
            )
    _SetZAxisProperties(n_segmentations, time_stretching, axes)


def _ShowSegmentationsAsTunnels(
    segmentations: Sequence[array_t], time_stretching: float, axes: axes_3d_t, /
) -> None:
    """"""
    n_segmentations = segmentations.__len__()
    volume = nmpy.array(segmentations, dtype=nmpy.uint8)
    original_extents = (
        range(n_segmentations),
        range(volume.shape[1]),
        range(volume.shape[2]),
    )
    interpolated_extents = (
        nmpy.linspace(
            0, n_segmentations - 1, num=int(round(time_stretching * n_segmentations))
        ),
        *original_extents[1:],
    )
    all_times, all_rows, all_cols = nmpy.meshgrid(*interpolated_extents, indexing="ij")
    interpolated_sites = nmpy.vstack((all_times.flat, all_rows.flat, all_cols.flat)).T
    interpolated = ntrp.interpn(original_extents, volume, interpolated_sites)
    reshaped = nmpy.reshape(
        interpolated, (interpolated_extents[0].size, *volume.shape[1:])
    )
    reorganized = nmpy.moveaxis(reshaped, (0, 1, 2), (2, 0, 1))
    flipped = nmpy.flip(reorganized, axis=2)
    vertices, faces, *_ = msre.marching_cubes(flipped, 0.5, step_size=5)
    axes.plot_trisurf(
        vertices[:, 0],
        vertices[:, 1],
        faces,
        nmpy.amax(vertices[:, 2]) - vertices[:, 2],
        cmap="rainbow",
        lw=1,
    )
    _SetZAxisProperties(n_segmentations, time_stretching, axes)


def _AnnotateCells(
    segmentation: array_t, axes: pypl.Axes, /, *, elevation: float = None
) -> None:
    """"""
    if elevation is None:
        AnnotateCell = lambda _pos, _txt: axes.annotate(
            _txt,
            _pos,
            ha="center",
            fontsize="x-small",
            color="red",
        )

        annotations = (
            _chd for _chd in axes.get_children() if isinstance(_chd, text.Annotation)
        )
        for annotation in annotations:
            annotation.remove()
    else:
        AnnotateCell = lambda _pos, _txt: axes.text(
            *_pos, _txt, fontsize="x-small", color="red"
        )

    labeled = msre.label(segmentation, connectivity=1)
    cells_properties = msre.regionprops(labeled)
    for properties in cells_properties:
        if elevation is None:
            position = nmpy.flipud(properties.centroid)
        else:
            position = (*properties.centroid, elevation)
        AnnotateCell(position, str(properties.label))


def ShowTracking(
    sequence: sequence_t,
    /,
    *,
    with_labels: bool = True,
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
    max_time_point = 0
    for t_idx, track in enumerate(sequence.TracksIterator()):
        color_idx = t_idx % colors.__len__()

        for time_point, src_cell, tgt_cell, is_final in track.SegmentsIterator():
            time_points = (time_point, time_point + 1)
            rows = (src_cell.centroid[0], tgt_cell.centroid[0])
            cols = (src_cell.centroid[1], tgt_cell.centroid[1])
            if time_points[1] > max_time_point:
                max_time_point = time_points[1]

            axes.plot3D(rows, cols, time_points, colors[color_idx])

            if with_labels:
                labels = (src_cell.label, tgt_cell.label)
                if is_final:
                    indices = (0, 1)
                else:
                    indices = (0,)
                for c_idx in indices:
                    axes.text(
                        rows[c_idx],
                        cols[c_idx],
                        time_points[c_idx],
                        str(labels[c_idx]),
                        fontsize="x-small",
                        color=colors[color_idx],
                    )
    _SetZAxisProperties(max_time_point + 1, 1.0, axes)

    _FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


def _SetZAxisProperties(
    n_segmentations: int, time_stretching: float, axes: axes_3d_t
) -> None:
    """"""
    z_max = time_stretching * (n_segmentations - 1)
    axes.set_zlim(0, z_max)
    axes.set_zticks(nmpy.linspace(0.0, z_max, num=n_segmentations))
    axes.set_zticklabels(str(_idx) for _idx in range(n_segmentations))


def ShowCellFeatureEvolution(
    sequence: sequence_t,
    feature: str,
    /,
    *,
    show_and_wait: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> None:
    """"""
    figure = pypl.figure()
    axes = figure.add_subplot(111)
    axes.set_title(feature)

    longest_evolution = 0
    for c_idx, cell in enumerate(sequence.RootCells()):
        evolutions = sequence.CellFeatureEvolution(cell, True, feature)
        for e_idx, evolution in enumerate(evolutions):
            if e_idx > 0:
                label = f"{c_idx}.{e_idx}"
            else:
                label = str(c_idx)
            axes.plot(evolution, label=label)

            if (length := evolution.__len__()) > longest_evolution:
                longest_evolution = length
    _SetTimeAxisProperties(longest_evolution - 1, axes)
    axes.legend()

    _FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


def _SetTimeAxisProperties(highest_value: int, axes: pypl.Axes) -> None:
    """"""
    axes.set_xlim(0, highest_value)
    axes.set_xticks(range(highest_value + 1))
    axes.set_xticklabels(str(_idx) for _idx in range(highest_value + 1))


def _FinalizeDisplay(
    figure: pypl.Figure, figure_name: str, show_and_wait: bool, archiver: archiver_t, /
) -> None:
    """"""
    if archiver is not None:
        figure.canvas.draw_idle()
        archiver.Store(figure, figure_name)

    if show_and_wait:
        pypl.show()
