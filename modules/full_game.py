"""Play the actual full game."""
from modules.full_board import FullBoard
from modules.full_baseboard import BeyondBoardError, OccupiedCellError, \
    print_color, input_color
UI_C = (120, 255, 200)


def play_game():
    """Activate the game logic."""
    board = FullBoard()
    print_color("Game starts!", fg=UI_C)
    # select order
    while True:
        first = input_color("Who starts first? (ai/me)\n", fg=UI_C)
        if first == "ai" or first == "me":
            break
        print_color("Try again!", fg=UI_C)
    if first == "me":
        turn_flag = True
    else:
        turn_flag = False

    # start main loop
    print(f"{'=' * 5}\n{board}\n{'=' * 5}")
    while True:
        if turn_flag:
            # start player input loop
            while True:
                try:
                    turn = input_color("Your turn (two comma-separated "
                                       f"integers in range(0, "
                                       f"{board.DIM_HINT})): ", fg=UI_C)
                    turn = tuple(map(int, turn.split(",")))
                    assert len(turn) == 2, "Please provide only two ints!"
                    board.make_move(*turn, symbol=board.HUMAN)
                except ValueError:
                    print_color("Input should be of form: 2,1", fg=UI_C)
                except (AssertionError, BeyondBoardError,
                        OccupiedCellError) as e:
                    print_color(e.args[0], fg=UI_C)
                else:
                    print_color("Successful turn!",
                                fg=board.COLOR_MAP[board.HUMAN])
                    break
                print(f"{'='*5}\n{board}\n{'='*5}")
        else:
            # make ai move
            board.make_move(*board.get_ai_move(), symbol=board.AI)
            print_color("Calculating AI made its move!",
                        fg=board.COLOR_MAP[board.AI])
        print(f"{'='*5}\n{board}\n{'='*5}")

        # check game state; exit if over
        state = board.game_state()
        if state == board.HUMAN:
            print_color("\nYou win!", fg=board.COLOR_MAP[board.HUMAN])
            break
        elif state == board.AI:
            print_color("\nAI wins!", fg=board.COLOR_MAP[board.AI])
            break
        elif state == board.EMPTY:
            print_color("\nIt's a draw!", fg=board.COLOR_MAP[board.EMPTY])
            break
        else:
            turn_flag = not turn_flag
    print_color("Thank you for the game!", fg=UI_C)


if __name__ == '__main__':
    play_game()
