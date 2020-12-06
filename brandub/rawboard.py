import numpy as np


class RawBoard:
    """ A numpy array with a little extra functionality """

    def __init__(self, board_array=None, indices=None, skip_checks=False):
        """ board_array must be (3,7,7) with all zero-one entries.
        indices must be list of 3-tuples """

        self.__skip_checks = skip_checks

        assert board_array is None or indices is None, \
            "one of board_array or indices must be None"
        assert board_array is not None or indices is not None, \
            "one of board_array or indices must not be None"

        if board_array is not None:
            if not self.skip_checks:
                assert type(board_array) == np.ndarray, \
                    "board_array must be numpy.ndarray"
                assert board_array.shape == (3, 7, 7), \
                    "must have shape (3, 7, 7)"
                assert len(np.unique(board_array)) == 2, \
                    "more than 0 and 1 in array"
                assert 0 in np.unique(board_array), "no zeros in board_array"
                assert 1 in np.unique(board_array), "no ones in board_array"

            self.__shape = board_array.shape
            self.__raw_board = board_array

            raw_indices = np.where(self.raw_board == 1)
            self.__indices = [
                (raw_indices[0][i], raw_indices[1][i], raw_indices[2][i])
                for i in range(len(raw_indices[0]))
            ]
        else:
            if not self.skip_checks:
                assert type(indices) == list, "indices must be list"
                assert len(indices) > 0, "indices cannot be empty"
                assert all(type(ind) == tuple for ind in indices), \
                    "all indices must be tuples"
                assert all(len(ind) == 3 for ind in indices), \
                    "all indices must have length 3"
                assert all(
                    type(i) == int or type(i) == np.int64
                    for ind in indices
                    for i in ind), \
                    "all values in each index must be ints"
                assert min(i for ind in indices for i in ind) >= 0, \
                    "all indices must be >= 0"
                assert max(ind[0] for ind in indices) <= 2, \
                    "max value <= 2 for first position"
                assert max(ind[1] for ind in indices) <= 6, \
                    "max value <= 6 for second position"
                assert max(ind[2] for ind in indices) <= 6, \
                    "max value <= 6 for third position"

            self.__indices = indices
            board_array = np.zeros((3, 7, 7))
            for ind in indices:
                board_array[ind] = 1
            self.__raw_board = board_array

    def __eq__(self, other):
        """ determine equality based on nupy matrices"""
        return (self.raw_board == other.raw_board).all()

    def __getitem__(self, *args):
        return self.raw_board.__getitem__(*args)

    @property
    def indices(self):
        return self.__indices

    @property
    def raw_board(self):
        return self.__raw_board

    @property
    def shape(self):
        return self.__shape

    @property
    def skip_checks(self):
        return self.__skip_checks

    def flatten(self):
        return self.raw_board.flatten()
