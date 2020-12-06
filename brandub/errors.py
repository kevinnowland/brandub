""" errors used by various classes """


class UnsettableAttributeError(Exception):
    def __init__(self):
        super().__init__("can't set attribute explicitly once set")


class InvalidTeamNameError(Exception):
    def __init__(self):
        super().__init__("team name must be 'attack' or 'defense'")


class InvalidMoveError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
