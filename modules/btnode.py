"""Represent a tree node."""
from modules.baseboard import BaseBoard


class StateNode(BaseBoard):
    """Represents a tree node with BaseBoard functionality."""

    def __init__(self, state: list = None, last_pos: (int, int) = None,
                 last_symbol: str = None):
        """Initialize a node.

        :param state: current board state
        :param last_pos: previously empty position
        :param last_symbol: last placed symbol
        """
        super().__init__(state, last_pos, last_symbol)
        self.right = None
        self.left = None

    def set_children(self):
        """Generate two child nodes.

        If only one move is available, generate only left child.
        """
        if self.last_symbol == self.AI:
            symbol = self.HUMAN
        else:
            symbol = self.AI
        movea, moveb = self._get_random_moves()
        self.left = StateNode(self.state_copy())
        self.left.make_move(*movea, symbol=symbol)
        if moveb is not None:
            self.right = StateNode(self.state_copy())
            self.right.make_move(*moveb, symbol=symbol)
