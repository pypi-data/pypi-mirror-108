import dataclasses as dcls
from abc import ABC as abc_t
from abc import abstractmethod
from typing import Optional, Sequence

from cell_tracking_BC.type.cell import cell_t


@dcls.dataclass(repr=False, eq=False)
class context_t(abc_t):
    """
    Latest tracking context: it contains all the information about the cells of frame t required to continue the
    tracking with the cells of frame t+1. When the tracks have been extended to the cells of frame t+1, this context
    will store the information about the cells of frame t+1 to get ready for continuing the tracking with the cells of
    frame t+2. This information is called the permanent storage of the context. By default, the permanent storage is
    defined as the attribute cells, a sequence of cell_t, and the temporary storage is defined as the attribute
    next_cells. Additional permanent and temporary attributes will generally be needed by contexts. Note that all these
    attributes go by pair since the method Advance must at least move all the temporary attributes to their permanent
    counterparts. The default implementation already move next_cells to cells. New contexts are in charge of moving the
    other attributes after calling super().Advance(). Similarly, the method DiscoverNextCells temporarily stores the
    discovered cells in next_cells, and new contexts are in charge of computing and storing the others attributes after
    calling super().DiscoverNextCells(next_cells) (See below for more details about permanent and temporary storages.)
    """

    cells: Sequence[cell_t] = dcls.field(init=False, default=None)
    next_cells: Sequence[cell_t] = dcls.field(init=False, default=None)

    def DiscoverNextCells(self, next_cells: Sequence[cell_t]) -> None:
        """
        The tracking has been done up to frame t. This method is called when "discovering" the cells of frame t+1. It
        must "temporarily" store all the information about these cells required to extend the tracking.
        """
        self.next_cells = next_cells

    @abstractmethod
    def PredecessorOfCell(
        self, next_cell: cell_t, next_cell_idx: int
    ) -> Optional[cell_t]:
        """
        This method is called successively for all the cells of frame t+1 to extend the tracking track by track. It
        must look among the cells of frame t described in the permanent storage if one can be considered a predecessor
        of the given cell of frame t+1. If none, then it must return None, meaning that the current track ends.
        """
        pass

    def Advance(self) -> None:
        """
        This method is called after PredecessorOfCell has been called for all the cells of frame t+1. It must move the
        temporary storage about the cells of frame t+1 created in DiscoverNextCells to the permanent storage that will
        be used in the next tracking iteration that will deal with frame t+2.
        """
        self.cells = self.next_cells
