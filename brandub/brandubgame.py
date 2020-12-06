from .board import get_initial_board
from .errors import InvalidMoveError
from .gamehistory import GameHistory
from .gamestate import GameState
from .movement import move
from IPython.display import clear_output


class BrandubGame:
    """  object oriented class for playing a whole game """

    def __init__(self):

        initial_state = GameState(get_initial_board(), "attack")
        self.__game_history = GameHistory([initial_state], max_length=10)

    def __str__(self):
        return "\ncurrent board:\n" + str(self.game_history[-1].board)

    @property
    def current_player(self):
        return self.game_history[-1].whose_turn

    @property
    def game_history(self):
        return self.__game_history

    @property
    def attack_victory(self):
        return self.game_history[-1].attack_victory

    @property
    def defense_victory(self):
        return self.game_history[-1].defense_victory

    @property
    def is_draw(self):
        return self.game_history.is_draw

    @property
    def game_over(self):
        return self.attack_victory or self.defense_victory \
            or self.is_draw

    @property
    def whose_turn(self):
        return self.game_history[-1].whose_turn

    def move(self, piece_position, new_position):
        """ move a piece and change the game history """
        self.__game_history = move(piece_position,
                                   new_position,
                                   game_history=self.game_history)

    def run(self):
        """ run the game until it's over """
        really_quit = None
        while not self.game_over:
            try:
                clear_output()
                self.print_board()

                move_invalid = True
                while move_invalid:

                    piece_invalid = True
                    msg = self.whose_turn + ", please enter a piece position:"
                    while piece_invalid:
                        try:
                            input_pos = input(msg)
                            raw_piece_pos = self.get_raw_pos(input_pos)
                            piece_invalid = False
                        except AssertionError:
                            pass

                    position_invalid = True
                    msg = self.whose_turn + ", please enter new position:"
                    while position_invalid:
                        try:
                            input_new_pos = input(msg)
                            raw_new_pos = self.get_raw_pos(input_new_pos)
                            position_invalid = False
                        except AssertionError:
                            pass

                    try:
                        if self.whose_turn == "attack":
                            level = 0
                        if self.whose_turn == "defense":
                            if self.game_history[-1].board \
                                   .shadow_pretty[tuple(raw_piece_pos)] == 1:
                                level = 1
                            else:
                                level = 2

                        piece_position = (level,
                                          raw_piece_pos[0],
                                          raw_piece_pos[1])
                        new_position = (level, raw_new_pos[0], raw_new_pos[1])
                        self.move(piece_position, new_position)
                        move_invalid = False
                    except InvalidMoveError:
                        print("not a valid move")
                        pass
            except KeyboardInterrupt:
                really_quit = input("\nAre you sure you want to quit? (y/n):")
                if really_quit.lower() == 'y':
                    return None
                else:
                    really_quit = None
                    pass

        if really_quit is None:
            clear_output()
            self.print_board()
            if self.game_history.defense_victory:
                msg = """Game over!

                The monarch has escaped the wrath of the proletariat and has
                hidden in the forest!
                """
                print(msg)
            elif self.game_history.attack_victory:
                msg = """Game Over!

                The proletariat has deposed the monarch!
                """
                print(msg)
            elif self.game_history.is_draw:
                msg = """Game over!

                Stalemate! The country remains eternally divided."""
                print(msg)
            else:
                raise Exception("wait, how did we get here?")

    def print_board(self):
        b = self.game_history[-1].board.shadow_pretty
        horiz_bar = '   -----------------------------'
        print(horiz_bar)
        for i in range(b.shape[0]):
            print(' {} |'.format(7-i), end='')
            for j in range(b.shape[1]):
                if b[i, j] == -1:
                    print(' A |', end='')
                elif b[i, j] == 1:
                    print(' D |', end='')
                elif b[i, j] == 2:
                    print(' M |', end='')
                elif (i, j) in [(0, 0), (6, 0), (0, 6), (6, 6)] \
                        and b[i, j] == 0:
                    print(' F |', end='')
                elif (i, j) == (3, 3) and b[i, j] == 0:
                    print(' C |', end='')
                else:
                    print('   |', end='')
            print('\n'+horiz_bar)
        print('     A   B   C   D   E   F   G')

    @staticmethod
    def get_raw_pos(text_position):
        """ convert a chess style position to a 2D raw position """
        letter_convert = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6
        }

        number_convert = {
            '1': 6,
            '2': 5,
            '3': 4,
            '4': 3,
            '5': 2,
            '6': 1,
            '7': 0
        }

        assert len(text_position) == 2, "move must have two characters"

        letter = text_position[0].upper()
        assert letter in letter_convert.keys(), \
            "first character must be letter between A and G (inclusive)"

        number = text_position[1]
        assert number in number_convert.keys(), \
            "second character must be integer between 1 and 7 (inclusive)"

        return [number_convert[number], letter_convert[letter]]
