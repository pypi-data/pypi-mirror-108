from typing import Any, Sequence

import numpy as nmpy
import skimage.measure as msre
from cell_tracking_BC.type.cell import cell_t


array_t = nmpy.ndarray


SKIMAGE_MORPHOLOGICAL_PROPERTIES: Sequence[str]  # Set below


def CellArea(cell: cell_t) -> int:
    """"""
    bb_map = cell.BBMap()
    output = nmpy.count_nonzero(bb_map)

    return output


def CellSKImageMorphologicalProperties(cell: cell_t) -> Sequence[Any]:
    """"""
    output = []

    bb_map = cell.BBMap().astype(nmpy.int8)
    properties = msre.regionprops(bb_map)[0]
    for property in SKIMAGE_MORPHOLOGICAL_PROPERTIES:
        output.append(properties[property])

    return output


def AverageIntensityInCell(cell: cell_t, frame: array_t) -> float:
    """"""
    map_ = cell.Map(frame.shape)
    output = nmpy.mean(frame[map_]).item()

    return output


def _CellSKImageMorphologicalPropertyNames() -> Sequence[str]:
    """"""
    output = []

    dummy = nmpy.zeros((10, 10), dtype=nmpy.int8)
    dummy[4:7, 4:7] = 1
    properties = msre.regionprops(dummy)[0]

    for property in dir(properties):
        if (not property.startswith("_")) and hasattr(properties, property):
            output.append(property)

    return output


SKIMAGE_MORPHOLOGICAL_PROPERTIES = _CellSKImageMorphologicalPropertyNames()
