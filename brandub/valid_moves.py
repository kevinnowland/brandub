import numpy as np


def is_forest(position_2d):
    """ returns whether the first two coords of
    position_2d is a forest"""
    return position_2d[0] in [0, 6] and position_2d[1] in [0, 6]


def is_castle(position_2d):
    """ returns whether the first two coords of position_2d
    is a castle"""
    return position_2d[0] == 3 and position_2d[1] == 3


def find_valid_moves(board, position):
    """ find valid moves for the piece at the given position.
    this assumes there is a piece at the position.

    position must be tuple (i, j, k)"""
    is_pawn = position[0] < 2

    shadow = board.shadow
    pos_2d = np.array(position[1:])

    def check_direction(direction_vector):
        """ get valid moves in the given direction

        direction must be +/- [1, 0] or +/- [0, 1] numpy arrays
        """

        valid_moves = []

        coord = 0 if direction_vector[0] != 0 else 1
        positive_direction = direction_vector[coord] == 1
        end_value = 6 if positive_direction else 0

        keep_going = pos_2d[coord] != end_value
        i = 0
        while keep_going:
            i += 1

            new_pos = pos_2d + i * direction_vector

            # stop if run into a piece
            if shadow[tuple(new_pos)] == 1:
                break

            # ignore the castle
            if is_castle(new_pos):
                continue

            keep_going = new_pos[coord] != end_value

            # if pawn and at the wall, see if its a forest but don't add
            if not keep_going and is_pawn and is_forest(new_pos):
                break

            valid_moves.append(tuple(new_pos))

        return valid_moves

    direction_vectors = (
        np.array([1, 0]),
        np.array([-1, 0]),
        np.array([0, 1]),
        np.array([0, -1])
    )

    return [
        (position[0], vec[0], vec[1])
        for dvec in direction_vectors
        for vec in check_direction(dvec)
    ]
