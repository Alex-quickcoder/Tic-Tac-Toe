"""Error classes, helper print functions and BaseBoard."""
from random import sample
from typing import Optional
DIM = 3


class OccupiedCellError(Exception):
    """Raise if cell is occupied."""
    pass


class BeyondBoardError(Exception):
    """Raise if given indexes are out of the board's bounds."""
    pass


class BaseBoard:
    """Represent a base board without ai features."""
    # symbols for representation
    EMPTY = "-"
    HUMAN = "X"
    AI = "O"
    # dimensions of the board
    DIM_HINT = DIM
    # all possible tuples of indexes for win conditions
    _ROW_I = tuple(tuple((i, j) for i in range(DIM))
                   for j in range(DIM))
    _COL_I = tuple(tuple((i, j) for j in range(DIM))
                   for i in range(DIM))
    _DIAG_I = tuple(tuple((i, i) for i in j)
                    for j in (range(DIM), range(-DIM, 0)))
    CHECK_I = _ROW_I + _COL_I + _DIAG_I
    MOVES_NUM = 2

    def __init__(self, state: list = None, last_pos: (int, int) = None,
                 last_symbol: str = None):
        """Initialize a BaseBoard.

        :param state: initial state of the board
        :param last_pos: previously empty position
        :param last_symbol: last symbol placed
        """
        if state is None:
            self.state = [[self.EMPTY for i in range(DIM)]
                          for ii in range(DIM)]
        else:
            self.state = state
        self.last_pos = last_pos
        self.last_symbol = last_symbol

    def state_copy(self) -> list:
        """Copy entire state."""
        return [row.copy() for row in self.state]

    def game_state(self) -> Optional[str]:
        """Check if current state is a draw, a win or a normal state."""
        state = self.state
        if any(all(self.AI == state[i][j] for i, j in iset)
               for iset in self.CHECK_I):
            return self.AI
        elif any(all(self.HUMAN == state[i][j] for i, j in iset)
               for iset in self.CHECK_I):
            return self.HUMAN
        elif all(all(item != self.EMPTY for item in self.state[i])
                   for i in range(DIM)):
            return self.EMPTY
        else:
            return None

    def __repr__(self) -> str:
        return "\n".join(" ".join(row) for row in self.state)

    def get_free_cells(self) -> (int, int):
        """Yield all free cells in the current state."""
        for i in range(DIM):
            for ii in range(DIM):
                if self.state[i][ii] == self.EMPTY:
                    yield i, ii

    def make_move(self, pos_i: int, pos_ii: int, symbol: str = None):
        """Make a move in the current state.

        :param pos_i: row of the board
        :param pos_ii: column of the board
        :param symbol: symbol to place
        """
        if not(0 <= pos_i < DIM and 0 <= pos_ii < DIM):
            raise BeyondBoardError("Cell does not exist in the board, "
                                   "try again!")
        if self.state[pos_i][pos_ii] != self.EMPTY:
            raise OccupiedCellError("Cell is not empty, try again!")

        self.state[pos_i][pos_ii] = symbol
        self.last_symbol = symbol
        self.last_pos = (pos_i, pos_ii)

    def _get_random_moves(self) -> tuple:
        """Get two random moves from allowed.

        :return: two random moves - (int, int) tuples If only one move is
        left, return it and None instead of the second one.
        """
        free_cells = [cell for cell in self.get_free_cells()]
        if len(free_cells) == 1:
            return free_cells[0], None
        return sample(free_cells, k=self.MOVES_NUM)


def print_color(*args, fg=None, bg=None, sep=" ", end="\n"):
    """Print in color (fg - font, bg - background) in RGB."""
    color_map = f"\33["
    if fg:
        color_map += f"38;2;{fg[0]};{fg[1]};{fg[2]};"
    if bg:
        color_map += f"48;2;{bg[0]};{bg[1]};{bg[2]};"
    if not(bg or fg):
        color_map += "0;"
    color_map = color_map[:-1] + "m"
    print(f"{color_map}", end="")
    print(*args, sep=sep, end="")
    print('\33[0m', end=end)


def input_color(prompt, fg=None, bg=None):
    """Input in color RGB."""
    print_color(prompt, end="", fg=fg, bg=bg)
    return input()
