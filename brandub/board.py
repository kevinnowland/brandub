from .rawboard import RawBoard
import numpy as np


class InvalidTeamNameError(Exception):
    def __init__(self):
        super().__init__("team name must be 'attack' or 'defense'")


class Board:
    """ a 3x7x7 array """

    def __init__(self, raw_board, fully_validate_board=True):
        assert type(fully_validate_board) == bool, \
            "fully_validate_board must be bool"
        self.__fully_validate_board = fully_validate_board

        assert type(raw_board) == RawBoard, "board must be RawBoard"
        if self.fully_validate_board:
            self.validate_board(raw_board)
        self.__raw_board = raw_board

    def __eq__(self, other):
        return self.raw_board == other.raw_board

    def __str__(self):
        return str(self.shadow_pretty)

    @property
    def positions(self):
        return self.raw_board.indices

    @property
    def raw_board(self):
        return self.__raw_board

    @property
    def fully_validate_board(self):
        return self.__fully_validate_board

    @property
    def shadow(self):
        return self.raw_board[0] + self.raw_board[1] + self.raw_board[2]

    @property
    def shadow_pretty(self):
        return -1 * self.raw_board[0] + self.raw_board[1] \
            + 2 * self.raw_board[2]

    @staticmethod
    def validate_board(board):
        """ takes (3, 7, 7) numpy array and validates it as a
        brandub board.

        Note: can be in a position that will result in pieces
        being removed.
        """
        assert np.max(board[0] + board[1] + board[2]) == 1, \
            "some tile has more than 1 piece on it"
        assert np.sum(board[0]) <= 8, "more than 8 attacking pawns"
        assert np.sum(board[1]) <= 4, "more than 4 defending pawns"
        assert np.sum(board[2]) <= 1, "more than 1 monarch"
        assert board[0, 3, 3] + board[1, 3, 3] == 0, \
            "no pawns allowed in castle"
        num_pawns_in_forests = \
            board[0, 0, 0] + board[0, 6, 0] \
            + board[0, 0, 6] + board[0, 6, 6] \
            + board[1, 0, 0] + board[1, 6, 0] \
            + board[1, 0, 6] + board[1, 6, 6]
        assert num_pawns_in_forests == 0, "no pawns allowed in forests"

    def check_victory(self, team):
        """ check for victory for the given team.

        team must 'attack' or 'defense'."""
        if team == "defense":
            return self.raw_board[2, 0, 0] + self.raw_board[2, 6, 0] \
                + self.raw_board[2, 0, 6] + self.raw_board[2, 6, 6] == 1
        elif team == "attack":
            return np.sum(self.raw_board[2]) == 0
        else:
            raise InvalidTeamNameError
