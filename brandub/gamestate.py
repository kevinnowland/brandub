from .board import Board
from .errors import InvalidTeamNameError
from .valid_moves import find_valid_moves


class GameState:
    """ this class enhances the board with some more gameplay aspects.
    also validates the validity of the board slightly. """

    def __init__(self, board, whose_turn):

        assert type(board) == Board
        self.__board = board

        assert not (self.attack_victory and self.defense_victory), \
            "only one of attack and defense can win"

        assert whose_turn in ["attack", "defense"], \
            "whose_turn must be 'attack' or 'defense'"
        self.__whose_turn = whose_turn

    def __eq__(self, other):
        """ equality based on board state """
        return self.board == other.board \
            and self.whose_turn == other.whose_turn

    def __str__(self):
        return str(self.board.shadow_pretty)

    @property
    def board(self):
        return self.__board

    @property
    def possible_moves(self):
        if self.whose_turn == "attack":
            pos_index = [0]
        elif self.whose_turn == "defense":
            pos_index = [1, 2]
        else:
            raise InvalidTeamNameError

        return [
            (p, pp)
            for p in self.board.positions if p[0] in pos_index
            for pp in find_valid_moves(self.board, p)
        ]

    @property
    def attack_victory(self):
        return self.__check_victory("attack")

    @property
    def defense_victory(self):
        return self.__check_victory("defense")

    @property
    def has_winner(self):
        return self.attack_victory or self.defense_victory

    @property
    def whose_turn(self):
        return self.__whose_turn

    def __check_victory(self, team):
        return self.board.check_victory(team)
