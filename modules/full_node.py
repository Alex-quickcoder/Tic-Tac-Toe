"""Represent a full node."""
from modules.full_baseboard import FullBaseBoard


class FullStateNode(FullBaseBoard):
    """Represents a tree node with BaseBoard functionality."""

    def __init__(self, state: list = None, last_pos: (int, int) = None,
                 last_symbol: str = None):
        """Initialize a node.

        :param state: current board state
        :param last_pos: previously empty position
        :param last_symbol: last placed symbol
        """
        super().__init__(state, last_pos, last_symbol)
        self.children = []

    def set_children(self):
        """Generate two child nodes.

        If only one move is available, generate only left child.
        """
        if self.last_symbol == self.AI:
            symbol = self.HUMAN
        else:
            symbol = self.AI
        moves = self._get_random_moves()
        for move in moves:
            new_node = FullStateNode(self.state_copy())
            new_node.make_move(*move, symbol=symbol)
            self.children.append(new_node)
