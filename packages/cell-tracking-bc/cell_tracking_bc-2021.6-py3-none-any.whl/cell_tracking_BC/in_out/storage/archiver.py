from __future__ import annotations

import builtins as bltn
import dataclasses as dcls
import datetime as dttm
import json
from pathlib import Path as path_t
from typing import Any, Union

import matplotlib.pyplot as pypl
import numpy as nmpy
import tensorflow.keras as kras
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t


array_t = nmpy.ndarray


BUILTIN_TYPES = tuple(
    _typ for _elm in dir(bltn) if isinstance((_typ := getattr(bltn, _elm)), type)
)


@dcls.dataclass(repr=False, eq=False)
class archiver_t:

    folder: path_t = None

    @classmethod
    def NewForFolderAndSequence(
        cls, folder: Union[str, path_t], sequence: str, /
    ) -> archiver_t:
        """"""
        if isinstance(folder, str):
            folder = path_t(folder)
        for component in (sequence.replace(".", "_"), None):
            if folder.exists():
                if not folder.is_dir():
                    raise ValueError(
                        f"{folder}: Not a folder; Cannot be used by {cls.__name__.upper()}"
                    )
            else:
                folder.mkdir()
            if component is not None:
                folder /= component

        original_name = cls._TimeStamp()
        folder /= original_name
        version = 0
        while folder.exists():
            version += 1
            folder = folder.parent / f"{original_name}-{version}"
        folder.mkdir()

        instance = cls(folder)

        return instance

    def Store(
        self, element: Any, name: str, /, *, with_time_stamp: bool = True
    ) -> None:
        """"""
        should_log = isinstance(element, str) and name.endswith(".log")

        if with_time_stamp and not should_log:
            name += self.__class__._TimeStamp()

        if should_log:
            with open(self.folder / name, "a") as writer:
                writer.write(self._TimeStamp() + "\n")
                writer.write(element + "\n")
        elif type(element) in BUILTIN_TYPES:
            with open(self.folder / f"{name}.json", "w") as writer:
                json.dump(element, writer, indent=4)
        elif isinstance(element, array_t):
            nmpy.savez_compressed(self.folder / f"{name}.npz", contents=element)
        elif isinstance(element, pypl.Figure):
            element.savefig(self.folder / f"{name}.png")
        elif isinstance(element, pypl.Axes) or isinstance(element, axes_3d_t):
            element.figure.savefig(self.folder / f"{name}.png")
        elif isinstance(element, kras.Model):
            element.save(self.folder / name)
        else:
            raise ValueError(
                f"{type(element).__name__}: Type of {element} unprocessable by {self.__class__.__name__.upper()}"
            )

    @staticmethod
    def _TimeStamp() -> str:
        """"""
        return dttm.datetime.now().isoformat().replace(".", ":")
