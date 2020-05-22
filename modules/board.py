"""Represent a board with ai features."""
from modules.btree import StateTree
from modules.baseboard import BaseBoard, print_color


class Board(BaseBoard):
    """Represent a board with ai features."""
    # colors for text representation
    COLOR_MAP = {
        BaseBoard.HUMAN: (50, 150, 255),
        BaseBoard.AI: (255, 100, 100),
        BaseBoard.EMPTY: (255, 230, 55)
    }

    def get_ai_move(self, verbose: bool = False) -> (int, int):
        """Get ai move from the binary decision tree.

        :param verbose: whether to print the randomly chosen choices
        :return: likely a more optimal move
        """
        choice_a, choice_b = self._get_random_moves()
        if choice_b is None:
            return choice_a

        tree_a = StateTree(self, choice_a)
        tree_b = StateTree(self, choice_b)

        tree_a.build_tree()
        tree_b.build_tree()

        if verbose:
            print_color(f"Between {choice_a} and {choice_b} the better choice"
                        f" probably is...",
                        fg=self.COLOR_MAP[self.AI], end="")

        return max(tree_a, tree_b, key=lambda tr: tr.get_points()).choice

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
