"""Represent a decision tree."""
from modules.btnode import StateNode


class StateTree:
    """Represent a binary decision tree."""

    def __init__(self, board, choice: (int, int)):
        """Generate a binary decision tree.

        :param board: board to generate for
        :type board: Board
        :param choice: chosen move
        """
        new_state = board.state_copy()
        new_state[choice[0]][choice[1]] = board.AI
        self._root = StateNode(new_state)
        self._root.last_symbol = board.AI
        self._root.last_pos = choice

    @property
    def choice(self) -> (int, int):
        """Return initial chosen move."""
        return self._root.last_pos

    def build_tree(self):
        """Build the decision tree recursively."""
        def recursive_build(node: StateNode):
            """Build the tree starting from node.

            Build a branch while the game does not end.
            :param node: current parent node
            """
            if node is None or node.game_state() is not None:
                return None
            node.set_children()
            recursive_build(node.left)
            recursive_build(node.right)

        recursive_build(self._root)

    def get_points(self) -> int:
        """Get win points for the tree.

        Assign 1 point for ai victory, 0 for draw and -1 for loss and
        calculate their sum for the tree.
        :return: the sum of all points
        """
        def recurse_points(node: StateNode):
            """Calculate points starting from node.

            :param node: current node
            :return: sum of points points for current node as the root
            """
            if node is None:
                return 0
            state = node.game_state()
            if state is None:
                return recurse_points(node.left) + recurse_points(node.right)
            elif state == node.AI:
                return 1
            elif state == node.HUMAN:
                return -1
            else:
                return 0
        return recurse_points(self._root)
