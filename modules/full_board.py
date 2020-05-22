"""Represent a full board with ai features."""
from modules.full_tree import FullStateTree
from modules.full_baseboard import FullBaseBoard, print_color


class FullBoard(FullBaseBoard):
    """Represent a board with ai features."""

    # colors for text representation
    COLOR_MAP = {
        FullBaseBoard.HUMAN: (50, 150, 255),
        FullBaseBoard.AI: (255, 100, 100),
        FullBaseBoard.EMPTY: (255, 230, 55)
    }

    def get_ai_move(self) -> (int, int):
        """Get ai move from the binary decision tree.

        :return: likely a more optimal move
        Note: a better approach would be to use the Minimax algorythm
        """
        choices = self._get_random_moves()

        trees = []
        for choice in choices:
            new_tree = FullStateTree(self, choice)
            new_tree.build_tree()
            trees.append(new_tree)

        return max(trees, key=lambda tr: tr.get_points()).choice

    @staticmethod
    def _color_str(raw_str: str, color: (int, int, int)) -> str:
        """Color the string.

        :param raw_str: colorless string
        :param color: color in tuple RDG format
        :return: colored string
        """
        return (f"\33[38;2;{color[0]};{color[1]};{color[2]}m{raw_str}")

    def __str__(self) -> str:
        """Return a colored string representation."""
        colored = self.__repr__()
        color_map = self.COLOR_MAP
        for symbol in color_map:
            colored = colored.replace(symbol,
                                      self._color_str(symbol,
                                                      color_map[symbol]))
        return f"{colored}\33[0m"
