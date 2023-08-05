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

from __future__ import annotations

import dataclasses as dcls
from pathlib import Path as path_t
from typing import Any, Callable, Dict, Iterator, Optional, Sequence, Tuple, Union

import cell_tracking_BC.in_out.storage.sequence as sqio
import numpy as nmpy
from cell_tracking_BC.type.cell import cell_t
from cell_tracking_BC.type.frame import frame_t, transform_h
from cell_tracking_BC.type.tracks import track_t, tracks_t


array_t = nmpy.ndarray
channel_computation_h = Callable[[Any], array_t]


@dcls.dataclass(repr=False, eq=False)
class sequence_t:

    path: Optional[path_t] = None
    shape: Tuple[int, int] = None  # In case contents has been cleared to save memory
    frames_of_channel: Dict[str, Sequence[Union[array_t, frame_t]]] = None
    cell_channel: str = None  # Name of channel whose frames store the segmented cells
    nuclei_sgms: Sequence[array_t] = dcls.field(init=False, default=None)
    cytoplasms_sgms: Sequence[array_t] = dcls.field(init=False, default=None)
    cells_sgms: Sequence[array_t] = dcls.field(init=False, default=None)
    tracks: tracks_t = dcls.field(init=False, default=None)

    @classmethod
    def NewFromPath(
        cls,
        path: path_t,
        in_channel_names: Sequence[Optional[str]],
        first_frame: int = 0,
        last_frame: int = 999999,
        SequenceLoading: Callable[[path_t], array_t] = sqio.SequenceByITK,
    ) -> sequence_t:
        """
        in_channel_names: names equal to None or "___" or "---" indicate channels that should be discarded
        """
        # TODO: write several variants for path=folder with different hierarchies maybe
        n_in_channels = in_channel_names.__len__()

        frames_of_channel = {}
        for name in in_channel_names:
            if (name is not None) and (name != "___") and (name != "---"):
                frames_of_channel[name] = []
        out_channel_names = tuple(frames_of_channel.keys())

        frames = SequenceLoading(path)
        c_idx = n_in_channels - 1
        time_point = -1
        for raw_frame in frames:
            c_idx += 1
            if c_idx == n_in_channels:
                c_idx = 0
                time_point += 1

            if time_point < first_frame:
                continue
            elif time_point > last_frame:
                break

            name = in_channel_names[c_idx]
            if name in out_channel_names:
                # print(f"Frame {name}.{time_point}")
                frame = frame_t.NewFromArray(raw_frame)
                frames_of_channel[name].append(frame)

        shape = frames_of_channel[out_channel_names[0]][0].shape
        instance = cls(path, shape, frames_of_channel, out_channel_names[0])

        return instance

    @property
    def length(self) -> int:
        """"""
        return self.frames_of_channel[self.cell_channel].__len__()

    @property
    def base_channels(self) -> Sequence[str]:
        """
        Names of channels read from file (as opposed to computed channels)
        """
        return tuple(
            _nme
            for _nme, _frm in self.frames_of_channel.items()
            if isinstance(_frm[0], frame_t)
        )

    def Frames(
        self,
        /,
        *,
        channel: Union[str, Sequence[str]] = None,
        raw_mode: bool = True,
        as_iterator: bool = False,
    ) -> Union[Tuple[array_t, ...], Iterator[array_t], Iterator[Tuple[array_t, ...]]]:
        """
        channel: None=all (!) base channels; Otherwise, only (a) base channel name(s) can be passed
        as_iterator: Always considered True if channel is None or a sequence of channel names
        """
        if isinstance(channel, str):
            return self._FramesForSingleChannel(channel, raw_mode, as_iterator)
        else:
            return self._FramesForMultipleChannels(channel, raw_mode)

    def _FramesForSingleChannel(
        self, channel: str, raw_mode: bool, as_iterator: bool, /
    ) -> Union[Tuple[array_t, ...], Iterator[array_t]]:
        """"""
        frames = self.frames_of_channel[channel]
        if raw_mode:
            iterator = (_frm.contents for _frm in frames)
            if as_iterator:
                output = iterator
            else:
                output = tuple(iterator)
        else:
            output = frames

        return output

    def _FramesForMultipleChannels(
        self, channels: Optional[Sequence[str]], raw_mode: bool, /
    ) -> Iterator[Tuple[array_t, ...]]:
        """"""
        if channels is None:
            channels = tuple(self.base_channels)

        for f_idx in range(self.length):
            frames = (self.frames_of_channel[_chl][f_idx] for _chl in channels)
            if raw_mode:
                frames = (_frm.contents for _frm in frames)

            yield tuple(frames)

    def CellsIterator(self) -> Iterator[Sequence[cell_t]]:
        """"""
        frames = self.frames_of_channel[self.cell_channel]
        for frame in frames:
            yield frame.cells

    def CellFeatureEvolution(
        self, cell: cell_t, cell_is_root: bool, feature: str, /
    ) -> Sequence[Sequence[Any]]:
        """
        cell_is_root: Otherwise, cell is considered a leaf
        """
        if cell_is_root:
            FoundTracks = self.tracks.TracksFromRoot
        else:
            FoundTracks = lambda _cll: (self.tracks.TrackToLeaf(_cll),)

        output = []

        for track in FoundTracks(cell):
            evolution = tuple(_cll.features[feature] for _cll in track)
            output.append(evolution)

        return output

    def TracksIterator(self) -> Iterator[track_t]:
        """"""
        return self.tracks.TracksIterator()

    def ApplyTransform(
        self,
        Transform: transform_h,
        /,
        *,
        channel: Union[str, Sequence[str]] = None,
        with_reference: str = None,
    ) -> None:
        """
        channel: None=all (!)
        """
        if channel is None:
            channels = self.base_channels
        elif isinstance(channel, str):
            channels = (channel,)
        else:
            channels = channel

        if with_reference is None:
            for channel in channels:
                frames = self.frames_of_channel[channel]
                for frame in frames:
                    frame.ApplyTransform(Transform)
        else:
            to_be_transformed = tuple(
                _chl for _chl in channels if _chl != with_reference
            )
            frames_sets = self.Frames(
                channel=(with_reference, *to_be_transformed), raw_mode=False
            )
            for frames in frames_sets:
                reference_frame = frames[0].contents
                for frame in frames[1:]:
                    frame.ApplyTransform(Transform, with_reference=reference_frame)

    def AddComputedChannel(
        self, name: str, ChannelComputation: channel_computation_h
    ) -> None:
        """"""
        computed = []
        for raw_frames in self.Frames():
            computed.append(ChannelComputation(*raw_frames))

        self.frames_of_channel[name] = computed

    def AddCellsFromSegmentations(
        self,
        /,
        *,
        nuclei_sgms: Sequence[array_t] = None,
        cytoplasms_sgms: Sequence[array_t] = None,
        cells_sgms: Sequence[array_t] = None,
    ) -> None:
        """
        Segmentation are supposed to be binary (as opposed to already labeled)
        Valid options: See cell_t.AllCompartmentsFromSomeCompartments
        """
        self.nuclei_sgms = nuclei_sgms
        self.cytoplasms_sgms = cytoplasms_sgms
        self.cells_sgms = cells_sgms

        if nuclei_sgms is None:
            nuclei_sgms = self.length * [None]
        if cytoplasms_sgms is None:
            cytoplasms_sgms = self.length * [None]
        if cells_sgms is None:
            cells_sgms = self.length * [None]

        frames = self.frames_of_channel[self.cell_channel]
        parameters = {"nuclei_sgm": None, "cytoplasms_sgm": None, "cells_sgm": None}
        for frame, *segmentations in zip(
            frames,
            nuclei_sgms,
            cytoplasms_sgms,
            cells_sgms,
        ):
            parameters["nuclei_sgm"] = segmentations[0]
            parameters["cytoplasms_sgm"] = segmentations[1]
            parameters["cells_sgm"] = segmentations[2]
            frame.AddCellsFromSegmentations(**parameters)

    def AddTracks(self, tracks: tracks_t, when_fails: str = "raise") -> None:
        """
        when_fails: See track_t.IsConform
        """
        if tracks.IsConform(when_fails=when_fails):
            self.tracks = tracks

    def ClearContents(self):
        """
        To free up some memory when all processing has been done
        """
        for frames in self.frames_of_channel.values():
            if isinstance(frames[0], frame_t):
                for frame in frames:
                    frame.ClearContents()

    def __str__(self) -> str:
        """"""
        return (
            f"{self.__class__.__name__.upper()}.{id(self)}\n"
            f"{self.path=}\n"
            f"{self.shape=}\n"
            f"{tuple(self.frames_of_channel.keys())=}\n"
            f"{self.frames_of_channel[self.cell_channel].__len__()=}\n"
            f"{self.tracks=}"
        )
