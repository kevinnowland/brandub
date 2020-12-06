"""define movement and such"""

from .board import Board
from .errors import InvalidMoveError
from .gamehistory import GameHistory
from .gamestate import GameState
from .rawboard import RawBoard
from .valid_moves import find_valid_moves
import numpy as np


def is_piece_captured(raw_board, piece_position):
    """ determine if a piece at (i, j, k) is captured
    given the positions on a (3, 7, 7) numpy array
    raw_board.

    WARNING: This does not validate that the raw_board is a
    vaid raw_board. """
    i = piece_position[1]
    j = piece_position[2]

    topography_inds_corners = [(0, 0), (0, 6), (6, 0), (6, 6)]

    if piece_position[0] == 0 or piece_position[0] == 1:

        if piece_position[0] == 0:
            enemy_board = raw_board[1] + raw_board[2]
            topography_inds = topography_inds_corners + [(3, 3)]

        else:
            enemy_board = raw_board[0]

            if raw_board[2, 3, 3] == 0:
                # no monarch? then castle is threat
                topography_inds = topography_inds_corners + [(3, 3)]
            else:
                topography_inds = topography_inds_corners

        topography = np.zeros((7, 7))
        for ind in topography_inds:
            topography[ind] = 1
        bad_things = enemy_board + topography

        if i == 0 or i == 6:
            # on top or bottom (can't be in corner)
            return bad_things[i, j-1] == 1 and bad_things[i, j+1] == 1
        elif j == 0 or j == 6:
            # on left or right side (can't be in corner)
            return bad_things[i-1, j] == 1 and bad_things[i+1, j] == 1
        else:
            # otherwise just check
            if bad_things[i, j-1] == 1 and bad_things[i, j+1] == 1:
                return True
            elif bad_things[i+1, j] == 1 and bad_things[i-1, j] == 1:
                return True
            else:
                return False

    elif piece_position[0] == 2:

        enemy_board = raw_board[0]

        if i != 3 or j != 3:
            topography_inds = topography_inds_corners + [(3, 3)]
        else:
            topography_inds = topography_inds_corners

        topography = np.zeros((7, 7))
        for ind in topography_inds:
            topography[ind] = 1
        bad_things = enemy_board + topography

        if (i, j) in [(3, 2), (3, 3), (3, 4), (2, 3), (4, 3)]:
            # in or next to castle have to be surrounded
            return bad_things[i+1, j] == 1 and bad_things[i-1, j] == 1 \
                and bad_things[i, j+1] == 1 and bad_things[i, j-1] == 1
        else:
            if (i, j) in [(0, 0), (0, 6), (6, 0), (6, 6)]:
                # safe in corner
                return False
            elif i == 0 or i == 6:
                # top or bottom: non corner
                return bad_things[i, j+1] == 1 and bad_things[i, j-1] == 1
            elif j == 0 or j == 6:
                # left or right: non corner
                return bad_things[i+1, j] == 1 and bad_things[i-1, j] == 1
            else:
                # any other spot on board
                if bad_things[i+1, j] == 1 and bad_things[i-1, j] == 1:
                    return True
                elif bad_things[i, j+1] == 1 and bad_things[i, j-1] == 1:
                    return True
                else:
                    return False
    else:
        msg = "piece_position[0] must be 0, 1, 2: {}".format(piece_position[0])
        raise Exception(msg)


def remove_captured_pieces(raw_board):
    """ take a raw (3, 7, 7) board and remove any
    captured pieces.

    Returns a raw_board """

    # get captured_pieces
    remaining_positions = [
        piece_position for piece_position in raw_board.indices
        if not is_piece_captured(raw_board, piece_position)
    ]

    return RawBoard(indices=remaining_positions,
                    skip_checks=raw_board.skip_checks)


def move(piece_position, new_position, board=None,
         game_state=None, game_history=None):
    """
    create a new board by moving the piece at
    piece_position to new_position and clearing
    off any captured pieces.

    piece_position and new_position should
    be (i, j, k) tuples.
    """

    if board is not None:
        assert game_state is None and game_history is None, \
            "only one of board, game_state, game_history can be provided"
    elif game_state is not None:
        assert game_history is None, \
            "only one of board, game_state, game_history can be provided"
        board = game_state.board
    else:
        assert game_history is not None, \
            "only one of board, game_state, game_history can be provided"
        assert len(game_history) != 0, "game_history cannot be empty"
        board = game_history[-1].board

    if board.raw_board[piece_position] == 0:
        raise InvalidMoveError("noi piece at requested permission")

    if game_state is not None or game_history is not None:
        if game_state is not None:
            team = game_state.whose_turn
        else:
            team = game_history[-1].whose_turn

        if team == "attack":
            assert piece_position[0] == 0, \
                "attacker must move attacking pawns"
        else:
            assert piece_position[0] == 1 or piece_position[0] == 2, \
                "defender must move defending pawns or monarch"

    if new_position not in find_valid_moves(board, piece_position):
        raise InvalidMoveError("piece cannot move there")

    # make the move
    new_positions = [p for p in board.positions if p != piece_position] \
        + [new_position]
    new_raw_board = RawBoard(indices=new_positions,
                             skip_checks=board.raw_board.skip_checks)

    # remove pieces
    clean_raw_board = remove_captured_pieces(new_raw_board)
    new_board = Board(clean_raw_board, board.fully_validate_board)

    if game_state is None and game_history is None:
        return new_board
    elif game_state is not None:
        if game_state.whose_turn == "attack":
            whose_turn = "defense"
        else:
            whose_turn = "attack"
        return GameState(new_board, whose_turn)
    else:
        game_state = game_history[-1]

        if game_state.whose_turn == "attack":
            whose_turn = "defense"
        else:
            whose_turn = "attack"
        new_game_state = GameState(new_board, whose_turn)

        if len(game_history) == game_history.max_length:
            new_game_states = game_history.game_states[1:] + [new_game_state]
        else:
            new_game_states = game_history.game_states + [new_game_state]

        return GameHistory(new_game_states, game_history.max_length)
