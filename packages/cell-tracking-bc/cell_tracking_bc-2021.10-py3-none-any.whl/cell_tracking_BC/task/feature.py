from typing import Any, Sequence

import numpy as nmpy
import skimage.measure as msre
from cell_tracking_BC.type.cell import cell_t


array_t = nmpy.ndarray


SKIMAGE_MORPHOLOGICAL_FEATURES: Sequence[str]  # Set below


def CellArea(cell: cell_t) -> int:
    """"""
    bb_map = cell.BBMap()
    output = nmpy.count_nonzero(bb_map)

    return output


def CellSKImageMorphologicalFeatures(cell: cell_t) -> Sequence[Any]:
    """"""
    output = []

    bb_map = cell.BBMap().astype(nmpy.int8)
    features = msre.regionprops(bb_map)[0]
    for name in SKIMAGE_MORPHOLOGICAL_FEATURES:
        output.append(features[name])

    return output


def AverageIntensityInCell(cell: cell_t, frame: array_t) -> float:
    """"""
    map_ = cell.Map(frame.shape)
    output = nmpy.mean(frame[map_]).item()

    return output


def _CellSKImageMorphologicalFeatureNames() -> Sequence[str]:
    """"""
    output = []

    dummy = nmpy.zeros((10, 10), dtype=nmpy.int8)
    dummy[4:7, 4:7] = 1
    features = msre.regionprops(dummy)[0]

    for name in dir(features):
        if (not name.startswith("_")) and hasattr(features, name):
            output.append(name)

    return output


SKIMAGE_MORPHOLOGICAL_FEATURES = _CellSKImageMorphologicalFeatureNames()
